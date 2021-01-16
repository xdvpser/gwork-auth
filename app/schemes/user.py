from fastapi_users import models
from pydantic import validator


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    @validator("password")
    def valid_password(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password should be at least 8 characters")
        return password


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass
