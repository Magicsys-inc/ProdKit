from .auth_routing import DocumentedAuthSubjectAPIRoute
from .db_routing import AutoCommitAPIRoute, get_api_router_class


class APIRoute(AutoCommitAPIRoute, DocumentedAuthSubjectAPIRoute):
    pass


APIRouter = get_api_router_class(APIRoute)

__all__ = ["APIRouter"]
