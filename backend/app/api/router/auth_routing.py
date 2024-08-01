# # Based on: https://github.com/polarsource/polar/blob/main/server/polar/auth/routing.py

# from collections.abc import Callable
# from typing import Any, Union, get_args, get_origin, get_type_hints

from fastapi.routing import APIRoute

# from app.infra.config import settings
# from app.providers.auth.authn.models import AuthSubject


# def get_allowed_values(param_type: type) -> set[type]:
#     if get_origin(param_type) is Union:
#         return set(get_args(param_type))
#     else:
#         return {param_type}


class DocumentedAuthSubjectAPIRoute(APIRoute):
    """
    A subclass of `APIRoute` that automatically
    documents the allowed subjects for the endpoint.
    """

    pass


__all__ = ["DocumentedAuthSubjectAPIRoute"]
