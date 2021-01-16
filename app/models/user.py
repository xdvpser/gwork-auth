from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from app.db.base_class import Base
from app.db.session import database
from app.schemes.user import UserDB


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


user_db = SQLAlchemyUserDatabase(UserDB, database, UserTable.__table__)
