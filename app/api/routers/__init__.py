from app.api.routers.auth import get_auth_router  # noqa: F401
from app.api.routers.common import ErrorCode  # noqa: F401
from app.api.routers.register import get_register_router  # noqa: F401
from app.api.routers.reset import get_reset_password_router  # noqa: F401
from app.api.routers.users import get_users_router  # noqa: F401
from app.api.routers.verify import get_verify_router  # noqa: F401

try:
    from app.api.routers.oauth import get_oauth_router  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    pass
