from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(UserRegister):
    pass


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(BaseModel):
    id: Optional[UUID4] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True


class User(UserInDBBase):
    joined_date: Optional[datetime]
    last_login_date: Optional[datetime]


class UserInDB(UserInDBBase):
    hashed_password: str
    joined_date: Optional[datetime]
    last_login_date: Optional[datetime]
