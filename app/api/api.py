from fastapi import APIRouter, Depends, Response

from app.api.singleton import FastAPIUsers
from app.core.auth.cookie import CookieAuthentication
from app.core.auth.jwt import JWTAuthentication
from app.core.tasks import (after_verification_request,
                            on_after_forgot_password, on_after_register)
from app.models.user import user_db
from app.schemes.user import User, UserCreate, UserDB, UserUpdate
from config.settings import settings

jwt_auth = JWTAuthentication(
    secret=settings.SECRET_KEY, lifetime_seconds=3600, tokenUrl="/api/auth/jwt/login"
)
cookie_auth = CookieAuthentication(secret=settings.SECRET_KEY, lifetime_seconds=3600)
fastapi_users = FastAPIUsers(
    user_db,
    [cookie_auth, jwt_auth],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

router = APIRouter()


@router.post("/jwt/refresh", tags=["auth"])
async def refresh_jwt(
    response: Response, user=Depends(fastapi_users.get_current_active_user)
):
    return await jwt_auth.get_login_response(user, response)


router.include_router(
    fastapi_users.get_auth_router(jwt_auth), prefix="/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_auth_router(cookie_auth), prefix="/cookie", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(on_after_register), tags=["auth"]  # type: ignore
)
router.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET_KEY,
        after_forgot_password=on_after_forgot_password,  # type: ignore
    ),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(
        settings.SECRET_KEY,
        after_verification_request=after_verification_request,  # type: ignore
    ),
    tags=["auth"],
)
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
