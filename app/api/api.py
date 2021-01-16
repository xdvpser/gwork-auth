from fastapi import APIRouter, Depends, Response

from app.api.deps import cookie_auth, fastapi_users, jwt_auth
from app.api.post_tasks import (after_verification_request,
                                on_after_forgot_password, on_after_register)
from config.settings import settings

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
    fastapi_users.get_register_router(on_after_register), tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET_KEY, after_forgot_password=on_after_forgot_password
    ),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(
        settings.SECRET_KEY, after_verification_request=after_verification_request
    ),
    tags=["auth"],
)
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
