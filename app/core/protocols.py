from typing import Awaitable, Type

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

from pydantic import EmailStr

from app.crud.base import BaseUserDatabase
from app.schemes import user
from app.security import get_password_hash


class UserAlreadyExists(Exception):
    pass


class UserNotExists(Exception):
    pass


class UserAlreadyVerified(Exception):
    pass


class CreateUserProtocol(Protocol):  # type: ignore
    def __call__(
        self,
        user: user.BaseUserCreate,
        safe: bool = False,
        is_active: bool = None,
        is_verified: bool = None,
    ) -> Awaitable[user.BaseUserDB]:  # type: ignore
        pass


def get_create_user(
    user_db: BaseUserDatabase[user.BaseUserDB],
    user_db_model: Type[user.BaseUserDB],
) -> CreateUserProtocol:
    async def create_user(
        user: user.BaseUserCreate,
        safe: bool = False,
        is_active: bool = None,
        is_verified: bool = None,
    ) -> user.BaseUserDB:
        existing_user = await user_db.get_by_email(user.email)

        if existing_user is not None:
            raise UserAlreadyExists()

        hashed_password = get_password_hash(user.password)
        user_dict = (
            user.create_update_dict() if safe else user.create_update_dict_superuser()
        )
        db_user = user_db_model(**user_dict, hashed_password=hashed_password)
        return await user_db.create(db_user)

    return create_user  # type: ignore


class VerifyUserProtocol(Protocol):  # type: ignore
    def __call__(
        self, user: user.BaseUserDB
    ) -> Awaitable[user.BaseUserDB]:  # type: ignore
        pass


def get_verify_user(
    user_db: BaseUserDatabase[user.BaseUserDB],
) -> VerifyUserProtocol:
    async def verify_user(user: user.BaseUserDB) -> user.BaseUserDB:
        if user.is_verified:
            raise UserAlreadyVerified()

        user.is_verified = True
        return await user_db.update(user)

    return verify_user  # type: ignore


class GetUserProtocol(Protocol):  # type: ignore
    def __call__(
        self, user_email: EmailStr
    ) -> Awaitable[user.BaseUserDB]:  # type: ignore
        pass


def get_get_user(
    user_db: BaseUserDatabase[user.BaseUserDB],
) -> GetUserProtocol:
    async def get_user(user_email: EmailStr) -> user.BaseUserDB:
        if not (user_email == EmailStr(user_email)):
            raise UserNotExists()

        user = await user_db.get_by_email(user_email)

        if user is None:
            raise UserNotExists()

        return user

    return get_user  # type: ignore
