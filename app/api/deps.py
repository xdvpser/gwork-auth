from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (CookieAuthentication,
                                          JWTAuthentication)

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
