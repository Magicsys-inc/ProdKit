# Based on: https://github.com/polarsource/polar/blob/main/server/polar/kit/routing.py

from collections.abc import Callable

# from functools import wraps
from typing import Any, ParamSpec, TypeVar

from fastapi import APIRouter as _APIRouter
from fastapi.routing import APIRoute

# from app.infra.core.postgres import AsyncSession


class AutoCommitAPIRoute(APIRoute):
    """
    A subclass of `APIRoute` that automatically
    commits the session after the endpoint is called.

    It allows to directly return ORM objects from the endpoint
    without having to call `session.commit()` before returning.
    """

    pass


_P = ParamSpec("_P")
_T = TypeVar("_T")


def _inherit_signature_from(
    _to: Callable[_P, _T],
) -> Callable[[Callable[..., _T]], Callable[_P, _T]]:
    return lambda x: x  # pyright: ignore


def get_api_router_class(route_class: type[APIRoute]) -> type[_APIRouter]:
    """
    Returns a subclass of `APIRouter` that uses the given `route_class`.
    """

    class _CustomAPIRouter(_APIRouter):
        @_inherit_signature_from(_APIRouter.__init__)
        def __init__(self, *args: Any, **kwargs: Any) -> None:  # type: ignore
            kwargs["route_class"] = route_class
            super().__init__(*args, **kwargs)

    return _CustomAPIRouter


__all__ = ["AutoCommitAPIRoute", "get_api_router_class"]
