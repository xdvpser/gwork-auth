import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR, TypeDecorator

from app.crud.crud_user import SQLAlchemyUserDatabase
from app.db.base_class import Base
from app.db.session import database
from app.schemes.user import UserDB


class GUID(TypeDecorator):  # pragma: no cover
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(36), storing as regular strings.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class UserTable(Base):
    id = Column(GUID, primary_key=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=72), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


user_db = SQLAlchemyUserDatabase(UserDB, database, UserTable.__table__)  # type: ignore
