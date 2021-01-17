from typing import Callable, Optional

import jwt
from fastapi import APIRouter, Body, HTTPException, Request, status
from pydantic import UUID4, EmailStr

from app.api.routers.common import ErrorCode, run_handler
from app.crud.base import BaseUserDatabase
from app.schemes import user
from app.security import get_password_hash
from app.utils import JWT_ALGORITHM, generate_jwt

RESET_PASSWORD_TOKEN_AUDIENCE = "fastapi-users:reset"


def get_reset_password_router(
    user_db: BaseUserDatabase[user.BaseUserDB],
    reset_password_token_secret: str,
    reset_password_token_lifetime_seconds: int = 3600,
    after_forgot_password: Optional[Callable[[user.UD, str, Request], None]] = None,
    after_reset_password: Optional[Callable[[user.UD, Request], None]] = None,
) -> APIRouter:
    """Generate a router with the reset password routes."""
    router = APIRouter()

    @router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
    async def forgot_password(
        request: Request, email: EmailStr = Body(..., embed=True)
    ):
        user = await user_db.get_by_email(email)

        if user is not None and user.is_active:
            token_data = {"user_id": str(user.id), "aud": RESET_PASSWORD_TOKEN_AUDIENCE}
            token = generate_jwt(
                token_data,
                reset_password_token_lifetime_seconds,
                reset_password_token_secret,
            )
            if after_forgot_password:
                await run_handler(after_forgot_password, user, token, request)

        return None

    @router.post("/reset-password")
    async def reset_password(
        request: Request, token: str = Body(...), password: str = Body(...)
    ):
        try:
            data = jwt.decode(
                token,
                reset_password_token_secret,
                audience=RESET_PASSWORD_TOKEN_AUDIENCE,
                algorithms=[JWT_ALGORITHM],
            )
            user_id = data.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )

            try:
                user_uiid = UUID4(user_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )

            user = await user_db.get(user_uiid)
            if user is None or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )

            user.hashed_password = get_password_hash(password)
            await user_db.update(user)
            if after_reset_password:
                await run_handler(after_reset_password, user, request)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
            )

    return router
