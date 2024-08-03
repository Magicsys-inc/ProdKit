import dataclasses
from collections.abc import Sequence
from typing import Protocol

from starlette.datastructures import Headers
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send


class CORSMatcher(Protocol):
    def __call__(self, origin: str, scope: Scope) -> bool: ...


@dataclasses.dataclass
class CORSConfig:
    matcher: CORSMatcher
    allow_origins: Sequence[str] = ()
    allow_methods: Sequence[str] = ("GET",)
    allow_headers: Sequence[str] = ()
    allow_credentials: bool = False
    allow_origin_regex: str | None = None
    expose_headers: Sequence[str] = ()
    max_age: int = 600

    def get_middleware(self, app: ASGIApp) -> CORSMiddleware:
        return CORSMiddleware(
            app=app,
            allow_origins=self.allow_origins,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
            allow_credentials=self.allow_credentials,
            allow_origin_regex=self.allow_origin_regex,
            expose_headers=self.expose_headers,
            max_age=self.max_age,
        )


class CORSMatcherMiddleware:
    def __init__(
        self, app: ASGIApp, *, configs: dict[str, Sequence[CORSConfig]]
    ) -> None:
        self.app = app
        self.tenant_middlewares = {
            tenant_id: tuple(
                (config, config.get_middleware(app)) for config in tenant_configs
            )
            for tenant_id, tenant_configs in configs.items()
        }
        # Handle default (non-tenant-based) configurations separately
        self.default_middlewares = tuple(
            (config, config.get_middleware(app))
            for config in configs.get("default", [])
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        headers = Headers(scope=scope)
        origin = headers.get("origin")
        tenant_id = scope.get("tenant_id")  # Retrieve tenant_id from scope

        if origin is None:
            await self.app(scope, receive, send)
            return

        if tenant_id is None:
            # Use default configurations if no tenant ID
            tenant_middlewares = self.default_middlewares
        else:
            tenant_middlewares = self.tenant_middlewares.get(
                tenant_id, self.default_middlewares
            )

        middleware = self._get_config_middleware(origin, scope, tenant_middlewares)
        if middleware is None:
            await self.app(scope, receive, send)
            return

        if method == "OPTIONS" and "access-control-request-method" in headers:
            response = middleware.preflight_response(request_headers=headers)
            await response(scope, receive, send)
            return
        await middleware.simple_response(scope, receive, send, request_headers=headers)

    def _get_config_middleware(
        self,
        origin: str,
        scope: Scope,
        middlewares: Sequence[tuple[CORSConfig, CORSMiddleware]],
    ) -> CORSMiddleware | None:
        for config, middleware in middlewares:
            if config.matcher(origin, scope):
                return middleware
        return None


__all__ = ["CORSConfig", "CORSMatcherMiddleware", "Scope"]
