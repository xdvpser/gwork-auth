import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from pydantic.networks import AnyUrl


class RabbitmqDsn(AnyUrl):
    allowed_schemes = {"amqp"}


class Base(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),  # type: ignore
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_URL: Optional[RabbitmqDsn] = None

    @validator("RABBITMQ_URL", pre=True)
    def assemble_rmq_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RabbitmqDsn.build(
            scheme="amqp",
            user=values.get("RABBITMQ_USER"),
            password=values.get("RABBITMQ_PASSWORD"),
            host=values.get("RABBITMQ_HOST"),  # type: ignore
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
