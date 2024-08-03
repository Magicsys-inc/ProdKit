# Base source: https://github.com/polarsource/polar/blob/main/server/polar/middlewares.py

import functools
import re
from collections.abc import Awaitable, Callable
from os import environ
from urllib.parse import urlparse

import structlog
from fastapi import FastAPI, Request, Response
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.infra.config import settings
from app.infra.core.context import TenantContext
from app.infra.core.worker import flush_enqueued_jobs
from app.providers.monitoring.logging import Logger, generate_correlation_id


class LogCorrelationIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        structlog.contextvars.bind_contextvars(
            correlation_id=generate_correlation_id(),
            method=scope["method"],
            path=scope["path"],
        )

        try:
            await self.app(scope, receive, send)

        finally:
            structlog.contextvars.unbind_contextvars("correlation_id", "method", "path")


class XForwardedHostMiddleware:
    """
    Ensures the app respects the `X-Forwarded-Host` if correctly trusted.

    Necessary to make `.url_for` correctly working behind a proxy.

    Should not be necessary anymore when Uvicorn releases this:
    https://github.com/encode/uvicorn/pull/2231
    """

    def __init__(self, app: ASGIApp, trusted_hosts: str | list[str] = "127.0.0.1"):
        self.app = app
        if isinstance(trusted_hosts, str):
            self.trusted_hosts = {item.strip() for item in trusted_hosts.split(",")}
        else:
            self.trusted_hosts = set(trusted_hosts)
        self.always_trust = "*" in self.trusted_hosts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            client_addr: tuple[str, int] | None = scope.get("client")
            client_host = client_addr[0] if client_addr else None

            if self.always_trust or client_host in self.trusted_hosts:
                headers = MutableHeaders(scope=scope)

                if "x-forwarded-host" in headers:
                    headers.update({"host": headers["x-forwarded-host"]})
                    scope["headers"] = headers.raw

        return await self.app(scope, receive, send)


class FlushEnqueuedWorkerJobsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)

        if not settings.is_testing():
            await flush_enqueued_jobs(scope["state"]["arq_pool"])


class PathRewriteMiddleware:
    def __init__(
        self, app: ASGIApp, pattern: str | re.Pattern[str], replacement: str
    ) -> None:
        self.app = app
        self.pattern = pattern
        self.replacement = replacement
        self.logger: Logger = structlog.get_logger()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        scope["path"], replacements = re.subn(
            self.pattern, self.replacement, scope["path"]
        )

        if replacements > 0:
            self.logger.warning(
                "PathRewriteMiddleware",
                pattern=self.pattern,
                replacement=self.replacement,
                path=scope["path"],
            )

        send = functools.partial(self.send, send=send, replacements=replacements)
        await self.app(scope, receive, send)

    async def send(self, message: Message, send: Send, replacements: int) -> None:
        if message["type"] != "http.response.start":
            await send(message)
            return

        message.setdefault("headers", [])
        headers = MutableHeaders(scope=message)
        if replacements > 0:
            headers[f"x-{settings.app_name}-deprecation-notice"] = (
                "The API root has moved from /api/v1 to /v1. "
                "Please update your integration."
            )

        await send(message)


class TenantAwareMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    # TODO: Add a lightweight auth layer
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        headers = MutableHeaders(scope=request.scope)
        tenant_id = self.get_tenant_id(headers, request)
        sub_id = self.get_sub_id(headers, request)

        tenant_context = TenantContext(tenant_id=tenant_id, sub_id=sub_id)

        request.state.tenant_context = tenant_context

        response = await call_next(request)
        return response

    def get_tenant_id(self, headers: MutableHeaders, request: Request) -> str | None:
        # TODO: Correct it based on the header naming pattern
        tenant_id = self.extract_from_header(headers, "tenant-id")
        if tenant_id:
            return tenant_id

        tenant_id = self.extract_from_subdomain(request)
        if tenant_id:
            return tenant_id

        # Check URL path for tenant ID (assuming /tenant/{tenant_id}/... format)
        tenant_id = self.extract_from_path(request)
        if tenant_id:
            return tenant_id

        return None

    def extract_from_header(
        self, headers: MutableHeaders, header_name: str
    ) -> str | None:
        # TODO: Correct it based on the header naming pattern
        # headers = Headers(scope=request.scope)  # Use Headers to get request headers
        header_key = f"x-{settings.app_name}-{header_name}"
        return headers.get(header_key)

    def extract_from_subdomain(self, request: Request) -> str | None:
        host = request.headers.get("host", "")
        parts = host.split(".")
        if len(parts) > 2:
            return parts[0]
        return None

    def extract_from_path(self, request: Request) -> str | None:
        parsed_url = urlparse(request.url.path)
        parts = parsed_url.path.split("/")
        if len(parts) > 1 and parts[1]:
            return parts[1]
        return None

    def get_sub_id(self, headers: MutableHeaders, request: Request) -> str | None:
        sub_id = self.extract_from_header(headers, "sub-id")
        # TODO: Correct it based on the header naming pattern
        if sub_id:
            return sub_id
        return None


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(PathRewriteMiddleware, pattern=r"^/api/v1", replacement="/v1")
    app.add_middleware(FlushEnqueuedWorkerJobsMiddleware)
    app.add_middleware(
        XForwardedHostMiddleware,
        trusted_hosts=environ.get("FORWARDED_ALLOW_IPS", "127.0.0.1"),
    )
    app.add_middleware(LogCorrelationIdMiddleware)
    # app.add_middleware(TenantAwareMiddleware)
