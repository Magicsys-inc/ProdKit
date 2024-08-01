import contextlib
from collections.abc import AsyncGenerator
from typing import TypedDict

import structlog
from fastapi import FastAPI

from app.api.api import router
from app.api.openapi import OPENAPI_PARAMETERS
from app.infra.config import settings
from app.infra.core.cors import configure_cors

# from app.infra.core.db import lifespan
from app.infra.core.exceptions import add_exception_handlers
from app.infra.core.middleware import add_middlewares

# from app.providers.webhook.webhooks import app as webhook_app
# from app.infra.core.sentry import configure_sentry
# from app.infra.core.logfire import configure_logfire
# from app.infra.core.posthog import configure_posthog
# from app.infra.core.logfire import (
#     instrument_fastapi,
#     instrument_httpx,
#     instrument_sqlalchemy,
# )
from app.infra.core.worker import ArqRedis
from app.infra.core.worker import lifespan as worker_lifespan
from app.infra.kit.utils import generate_unique_openapi_id

# from app.providers.auth.oauth2.endpoints.well_known import router as well_known_router
# from app.providers.auth.oauth2.exception_handlers import (
#     OAuth2Error,
#     oauth2_error_exception_handler,
# )
from app.providers.monitoring.health import router as health_router
from app.providers.monitoring.logging import Logger
from app.providers.monitoring.logging import configure as configure_logging

log: Logger = structlog.get_logger()


class GlobalResourcesState(TypedDict):
    arq_pool: ArqRedis
    # monitoring configs
    # global cache connections
    # message brokers
    # etc.


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[GlobalResourcesState, None]:
    log.info(f"Starting {settings.APP_NAME} API")

    async with worker_lifespan() as arq_pool:
        log.info(f"{settings.APP_NAME} API started")

        yield {
            "arq_pool": arq_pool,
        }

        log.info(f"{settings.APP_NAME} API stopped")


def init_app() -> FastAPI:
    app = FastAPI(
        generate_unique_id_function=generate_unique_openapi_id,
        lifespan=lifespan,
        **OPENAPI_PARAMETERS,
    )

    configure_cors(app)

    add_middlewares(app)

    add_exception_handlers(app)

    # app.add_exception_handler(OAuth2Error, oauth2_error_exception_handler)  # pyright: ignore

    # /.well-known
    # app.include_router(well_known_router)

    # /healthz and /readyz
    app.include_router(health_router)

    app.include_router(router)

    # app.webhooks.routes = webhook_app.webhooks.routes

    return app


# configure_sentry()
# configure_logfire("backend")
configure_logging(logfire=True)
# configure_posthog()


app = init_app()
# instrument_fastapi(app)
# instrument_httpx()
