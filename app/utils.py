import json
from datetime import datetime, timedelta

import jwt
import pika

from config.settings import settings

params = pika.URLParameters(settings.RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="admin", body=json.dumps(body), properties=properties
    )


JWT_ALGORITHM = "HS256"


def generate_jwt(
    data: dict, lifetime_seconds: int, secret: str, algorithm: str = JWT_ALGORITHM
) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
    payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)  # type: ignore
