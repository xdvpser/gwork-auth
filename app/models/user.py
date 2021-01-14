from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base_class import Base


class User(Base):
    id = Column(UUID, primary_key=True, index=True)
    username = Column(String(length=64), index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # email = Column(String, unique=True, index=True, nullable=False)
    # is_email_verified = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    joined_date = Column(DateTime(timezone=True), server_default=func.now())
    last_login_date = Column(DateTime(timezone=True), onupdate=func.now())
