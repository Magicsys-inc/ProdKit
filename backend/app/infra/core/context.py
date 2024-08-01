import contextlib
from contextvars import ContextVar
from datetime import datetime
from types import TracebackType
from typing import ClassVar, Optional, TypedDict

from arq.connections import ArqRedis
from fastapi import Request
from pydantic import BaseModel

from app.data.dbs.postgres.postgres import AsyncEngine
from app.data.dbs.postgres.postgres import (
    AsyncSessionMaker as AsyncSessionMakerType,
)


class ProdkitContext:
    pass


class TenantContext:
    _contextvar: ClassVar[ContextVar[Optional["TenantContext"]]] = ContextVar(
        "TenantContext"
    )

    def __init__(self, tenant_id: str | None = None, sub_id: str | None = None):
        self.tenant_id = tenant_id
        self.sub_id = sub_id

    def __enter__(self) -> "TenantContext":
        self.token = TenantContext._contextvar.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        TenantContext._contextvar.reset(self.token)

    @classmethod
    def current(cls) -> "TenantContext":
        """Returns the current TenantContext, or None if there isn't one."""
        return TenantContext._contextvar.get(None) or TenantContext()

    # TODO: Do I need it here?
    @classmethod
    def get_tenant_context(cls, request: Request) -> Optional["TenantContext"]:
        """Retrieve TenantContext from request state from TenantAwareMiddleware."""
        return getattr(request.state, "tenant_context", None)

    def __repr__(self) -> str:
        return (
            f"<TenantContext tenant_id={self.tenant_id!r}, " f"sub_id={self.sub_id!r}>"
        )


class AccountContext:
    _contextvar: ClassVar[ContextVar[Optional["AccountContext"]]] = ContextVar(
        "AccountContext"
    )

    def __init__(self, account_id: str | None = None):
        self.account_id = account_id

    def __enter__(self) -> "AccountContext":
        self.token = AccountContext._contextvar.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        AccountContext._contextvar.reset(self.token)

    @classmethod
    def current(cls) -> "AccountContext":
        return AccountContext._contextvar.get(None) or AccountContext()

    def __repr__(self) -> str:
        return f"<AccountContext account_id={self.account_id!r}>"


class OrganizationContext:
    _contextvar: ClassVar[ContextVar[Optional["OrganizationContext"]]] = ContextVar(
        "OrganizationContext"
    )

    def __init__(self, organization_id: str | None = None):
        self.organization_id = organization_id

    def __enter__(self) -> "OrganizationContext":
        self.token = OrganizationContext._contextvar.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        OrganizationContext._contextvar.reset(self.token)

    @classmethod
    def current(cls) -> "OrganizationContext":
        return OrganizationContext._contextvar.get(None) or OrganizationContext()

    def __repr__(self) -> str:
        return f"<OrganizationContext organization_id={self.organization_id!r}>"


class UserContext:
    _contextvar: ClassVar[ContextVar[Optional["UserContext"]]] = ContextVar(
        "UserContext"
    )

    def __init__(self, user_id: str | None = None):
        self.user_id = user_id

    def __enter__(self) -> "UserContext":
        self.token = UserContext._contextvar.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        UserContext._contextvar.reset(self.token)

    @classmethod
    def current(cls) -> "UserContext":
        return UserContext._contextvar.get(None) or UserContext()

    def __repr__(self) -> str:
        return f"<UserContext user_id={self.user_id!r}>"


class ExecutionContext:
    _contextvar: ClassVar[ContextVar[Optional["ExecutionContext"]]] = ContextVar(
        "ExecutionContext"
    )

    # is_during_installation is True this is an event (or request) triggered by the app
    # or repository installation flow.
    #
    # It allows us to, for example, prevent creating notifications for objects
    # found during the initial syncing.
    is_during_installation: bool

    def __init__(
        self,
        is_during_installation: bool = False,
        tenant_context: TenantContext | None = None,
    ) -> None:
        self.is_during_installation = is_during_installation
        self.tenant_context = tenant_context or TenantContext.current()

    def __enter__(self) -> "ExecutionContext":
        self.token = ExecutionContext._contextvar.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ExecutionContext._contextvar.reset(self.token)

    @staticmethod
    def current() -> "ExecutionContext":
        """Returns the current ExecutionContext, or a clean one if there's no current
        context."""
        return ExecutionContext._contextvar.get(None) or ExecutionContext()

    def __repr__(self) -> str:
        return (
            f"<ExecutionContext is_during_installation={self.is_during_installation!r}, "
            f"tenant_context={self.tenant_context!r}>"
        )


# TODO: extended it to include tenant-specific configurations and states dynamically,
# possibly from a configuration service.
class ProdkitWorkerContext(BaseModel):
    is_during_installation: bool = False

    def to_execution_context(self) -> ExecutionContext:
        return ExecutionContext(is_during_installation=self.is_during_installation)


class WorkerContext(TypedDict):
    redis: ArqRedis
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMakerType


class JobContext(WorkerContext):
    job_id: str
    job_try: int
    enqueue_time: datetime
    score: int
    exit_stack: contextlib.ExitStack
    # logfire_span: logfire.LogfireSpan
