from collections.abc import Mapping, Sequence

from fastapi import FastAPI

from app.infra.config import settings
from app.infra.kit.cors import CORSConfig, CORSMatcherMiddleware, Scope

# class TenantCORSConfig:
#     def __init__(self, tenant_id: str, sub_id: str, origins: list[str]):
#         pass


def configure_cors(app: FastAPI) -> None:
    tenant_configs: dict[str, Sequence[CORSConfig]] = {}
    default_configs: list[CORSConfig] = []

    # Default CORS configurations
    if settings.CORS_ORIGINS:

        def prodkit_frontend_matcher(origin: str, scope: Scope) -> bool:
            return origin in settings.CORS_ORIGINS

        prodkit_frontend_config = CORSConfig(
            matcher=prodkit_frontend_matcher,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,  # Cookies are allowed
            allow_methods=["*"],  # TODO: Limit to common methods
            allow_headers=["*"],  # TODO: Limit to necessary headers
        )
        default_configs.append(prodkit_frontend_config)

    # External API calls CORS configuration
    api_config = CORSConfig(
        matcher=lambda origin, scope: True,
        allow_origins=["*"],
        allow_credentials=False,  # No cookies allowed
        allow_methods=["*"],  # TODO: Limit to common methods
        allow_headers=["Authorization"],  # Allow Authorization header to pass tokens
    )
    default_configs.append(api_config)

    # TODO: Make it being dynamic, rather than being hardcoded.
    tenant_configs = {
        # f"tenant{tenant_id}": [
        #     CORSConfig(
        #         matcher=lambda origin, scope: origin in allowed_origins,
        #         allow_origins=allowed_origins,
        #         allow_methods=allowed_methods,
        #         allow_headers=allowed_headers,
        #         allow_credentials=allowed_credentials,
        #     ),
        # ],
        # "tenant2": [
        #     CORSConfig(
        #         matcher=lambda origin, scope: origin in ["https://example2.com"],
        #         allow_origins=["https://example2.com"],
        #         allow_methods=["GET"],
        #         allow_headers=["*"],
        #         allow_credentials=False,
        #     ),
        # ],
        # ...
    }

    combined_configs: Mapping[str, Sequence[CORSConfig]] = {
        **tenant_configs,
        "default": default_configs,
    }

    app.add_middleware(CORSMatcherMiddleware, configs=combined_configs)
