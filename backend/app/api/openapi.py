from enum import StrEnum
from typing import Any, NotRequired, TypedDict

from app.infra.config import settings


class OpenAPIExternalDoc(TypedDict):
    description: NotRequired[str]
    url: str


class OpenAPITag(TypedDict):
    name: str
    description: NotRequired[str]
    externalDocs: NotRequired[dict[str, str]]


class APITag(StrEnum):
    """
    Tags used by our documentation to better organize the endpoints.

    They should be set after the "group" tag, which is used to group the endpoints
    in the generated documentation.

    **Example**

        ```py
        router = APIRouter(prefix="/products", tags=["products", APITag.featured])
        ```
    """

    documented = "documented"
    featured = "featured"

    @classmethod
    def metadata(cls) -> list[OpenAPITag]:
        return [
            {
                "name": cls.documented,
                "description": (
                    f"Endpoints shown and documented in the {settings.APP_NAME} API documentation."
                ),
            },
            {
                "name": cls.featured,
                "description": (
                    f"Endpoints featured in the {settings.APP_NAME} API documentation for their "
                    "interest in common use-cases."
                ),
            },
        ]


class OpenAPIParameters(TypedDict):
    title: str
    summary: str
    version: str
    description: str
    docs_url: str | None
    redoc_url: str | None
    openapi_tags: list[dict[str, Any]]


OPENAPI_PARAMETERS: OpenAPIParameters = {
    "title": f"{settings.APP_NAME} API",
    "summary": f"{settings.APP_NAME} HTTP and Webhooks API",
    "version": "0.1.0",
    "description": f"Read the docs at https://{settings.APP_URL}/docs/api-reference",
    "docs_url": None if settings.is_production() else "/docs",
    "redoc_url": None if settings.is_production() else "/redoc",
    "openapi_tags": APITag.metadata(),  # type: ignore
}

IN_DEVELOPMENT_ONLY = settings.is_development()

__all__ = ["OPENAPI_PARAMETERS", "IN_DEVELOPMENT_ONLY", "APITag"]
