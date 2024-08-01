# Base source: https://github.com/polarsource/polar/blob/main/server/polar/worker.py

import contextlib
import contextvars
import functools
import uuid
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Any, ParamSpec, TypeAlias, TypeVar, cast

# import logfire
import structlog
from arq import cron, func
from arq.connections import ArqRedis, RedisSettings
from arq.connections import create_pool as arq_create_pool
from arq.cron import CronJob
from arq.typing import OptionType, SecondsTimedelta, WeekdayOptionType
from arq.worker import Function

from app.data.dbs.postgres.postgres import (
    AsyncSession,
    SessionMakerFactory,
)
from app.infra.config import settings
from app.infra.core.context import (
    ExecutionContext,
    JobContext,
    ProdkitWorkerContext,
    TenantContext,
    WorkerContext,
)

# from app.infra.core.logfire import instrument_httpx, instrument_sqlalchemy
from app.infra.core.postgres import DatabaseEngine, SchemaName, get_schema_name
from app.providers.monitoring.logging import Logger, generate_correlation_id

log: Logger = structlog.get_logger()

JobToEnqueue: TypeAlias = tuple[str, tuple[Any], dict[str, Any]]
_jobs_to_enqueue = contextvars.ContextVar[list[JobToEnqueue]](
    f"{settings.app_name}_worker_jobs_to_enqueue", default=[]
)


class WorkerSettings:
    functions: list[Function] = []
    cron_jobs: list[CronJob] = []
    queue_name: str = settings.DEFAULT_QUEUE_NAME

    redis_settings = RedisSettings().from_dsn(settings.redis_url)

    @staticmethod
    async def on_startup(ctx: WorkerContext) -> None:
        log.info(f"{settings.app_name}.worker.startup")

        tenant_context = TenantContext.current()
        schema_name: SchemaName = get_schema_name(tenant_context.tenant_id)

        async_engine = DatabaseEngine.create_async_engine("worker", schema_name)
        async_sessionmaker = SessionMakerFactory.create_async_sessionmaker(async_engine)
        # instrument_sqlalchemy(async_engine.sync_engine)
        # instrument_httpx()

        ctx.update(
            {"async_engine": async_engine, "async_sessionmaker": async_sessionmaker}
        )

    @staticmethod
    async def on_shutdown(ctx: WorkerContext) -> None:
        engine = ctx["async_engine"]
        await engine.dispose()

        log.info(f"{settings.app_name}.worker.shutdown")

    @staticmethod
    async def on_job_start(ctx: JobContext) -> None:
        """
        Unfortunately, we don't have access to task arguments in this hook.

        This prevents us to implement things like common arguments handling, as we
        do for `request_correlation_id`.

        To circumvent this limitation, we implement this behavior
        through the `task_hooks` decorator.
        """
        exit_stack = contextlib.ExitStack()
        function_name = ":".join(ctx["job_id"].split(":")[0:-1])
        # logfire_span = exit_stack.enter_context(
        #     logfire.span("TASK {function_name}", function_name=function_name)
        # )
        ctx.update(
            {
                "exit_stack": exit_stack,
                # "logfire_span": logfire_span
            }
        )

    @staticmethod
    async def on_job_end(ctx: JobContext) -> None:
        """
        Unfortunately, we don't have access to task arguments in this hook.

        This prevents us to implement things like common arguments handling, as we
        do for `request_correlation_id`.

        To circumvent this limitation, we implement this behavior
        through the `task_hooks` decorator.
        """
        exit_stack = ctx["exit_stack"]
        exit_stack.close()


def enqueue_job(
    name: str,
    *args: Any,
    queue_name: str = settings.DEFAULT_QUEUE_NAME,
    **kwargs: Any,
) -> None:
    execution_context = ExecutionContext.current()
    prodkit_context = ProdkitWorkerContext(
        is_during_installation=execution_context.is_during_installation,
    )

    request_correlation_id = structlog.contextvars.get_contextvars().get(
        "correlation_id"
    )

    tenant_id = execution_context.tenant_context.tenant_id

    # Prefix job ID by task name by default
    _job_id = kwargs.pop("_job_id", f"{name}:{uuid.uuid4().hex}")

    kwargs = {
        "request_correlation_id": request_correlation_id,
        "prodkit_context": prodkit_context,
        "tenant_id": tenant_id,
        **kwargs,
        "_job_id": _job_id,
        "_queue_name": queue_name,
    }

    _jobs_to_enqueue_list = _jobs_to_enqueue.get([])
    _jobs_to_enqueue_list.append((name, args, kwargs))  # type: ignore
    _jobs_to_enqueue.set(_jobs_to_enqueue_list)

    log.debug(
        f"{settings.app_name}.worker.job_enqueued", name=name, args=args, kwargs=kwargs
    )


async def flush_enqueued_jobs(arq_pool: ArqRedis) -> None:
    if _jobs_to_enqueue_list := _jobs_to_enqueue.get([]):
        log.debug(f"{settings.app_name}.worker.flush_enqueued_jobs")
        for name, args, kwargs in _jobs_to_enqueue_list:
            await arq_pool.enqueue_job(name, *args, **kwargs)
            log.debug(
                f"{settings.app_name}.worker.job_flushed",
                name=name,
                args=args,
                kwargs=kwargs,
            )
        _jobs_to_enqueue.set([])


Params = ParamSpec("Params")
ReturnValue = TypeVar("ReturnValue")


def task_hooks(
    f: Callable[Params, Awaitable[ReturnValue]],
) -> Callable[Params, Awaitable[ReturnValue]]:
    @functools.wraps(f)
    async def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnValue:
        job_context = cast(JobContext, args[0])
        log_context: dict[str, Any] = {
            "correlation_id": generate_correlation_id(),
            "job_id": job_context["job_id"],
            "job_try": job_context["job_try"],
            "enqueue_time": job_context["enqueue_time"].isoformat(),
            "score": job_context["score"],
            "tenant_id": kwargs.get("tenant_id", None),
        }

        request_correlation_id = kwargs.pop("request_correlation_id", None)
        if request_correlation_id is not None:
            log_context["request_correlation_id"] = request_correlation_id

        structlog.contextvars.bind_contextvars(**log_context)
        # job_context["logfire_span"].set_attributes(log_context)

        log.info(f"{settings.app_name}.worker.job_started")
        r = await f(*args, **kwargs)

        arq_pool = job_context["redis"]
        await flush_enqueued_jobs(arq_pool)

        log.info(f"{settings.app_name}.worker.job_ended")
        structlog.contextvars.unbind_contextvars(
            "correlation_id",
            "request_correlation_id",
            "job_id",
            "job_try",
            "enqueue_time",
            "score",
            "tenant_id",
        )

        return r

    return wrapper


# TODO: Tenant-specific error handling and notification mechanisms to alert tenants of
# issues affecting their tasks.
def task(
    name: str,
    *,
    keep_result: SecondsTimedelta | None = None,
    timeout: SecondsTimedelta | None = None,
    keep_result_forever: bool | None = None,
    max_tries: int | None = None,
) -> Callable[
    [Callable[Params, Awaitable[ReturnValue]]], Callable[Params, Awaitable[ReturnValue]]
]:
    def decorator(
        f: Callable[Params, Awaitable[ReturnValue]],
    ) -> Callable[Params, Awaitable[ReturnValue]]:
        wrapped = task_hooks(f)

        new_task = func(
            wrapped,  # type: ignore
            name=name,
            keep_result=keep_result,
            timeout=timeout,
            keep_result_forever=keep_result_forever,
            max_tries=max_tries,
        )

        WorkerSettings.functions.append(new_task)

        return wrapped

    return decorator


def interval(
    *,
    month: OptionType = None,
    day: OptionType = None,
    weekday: WeekdayOptionType = None,
    hour: OptionType = None,
    minute: OptionType = None,
    second: OptionType = 0,
) -> Callable[
    [Callable[Params, Awaitable[ReturnValue]]], Callable[Params, Awaitable[ReturnValue]]
]:
    def decorator(
        f: Callable[Params, Awaitable[ReturnValue]],
    ) -> Callable[Params, Awaitable[ReturnValue]]:
        wrapped = task_hooks(f)

        new_cron = cron(
            wrapped,  # type: ignore
            month=month,
            day=day,
            weekday=weekday,
            hour=hour,
            minute=minute,
            second=second,
            run_at_startup=False,
        )

        # All crontabs are running on the "default" worker
        WorkerSettings.cron_jobs.append(new_cron)

        return wrapped

    return decorator


# TODO: Separate Redis queues per tenant
@contextlib.asynccontextmanager
async def lifespan() -> AsyncGenerator[ArqRedis, None]:
    arq_pool = await arq_create_pool(WorkerSettings.redis_settings)
    try:
        yield arq_pool
    finally:
        await arq_pool.close(True)


# TODO: Can be extended to dynamically select the appropriate schema
# configuration based on tenant information?
@contextlib.asynccontextmanager
async def AsyncSessionMaker(ctx: JobContext) -> AsyncGenerator[AsyncSession, None]:  # noqa: N802
    """Helper to open an AsyncSession context manager from the job context."""
    async with ctx["async_sessionmaker"]() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        else:
            await session.commit()


__all__ = [
    "WorkerSettings",
    "task",
    "lifespan",
    "enqueue_job",
    "JobContext",
    "AsyncSessionMaker",
    "ArqRedis",
]
