from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from config.settings import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


# def send_reset_password_email(email_to: str, email: str, token: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - Password recovery for user {email}"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
#         template_str = f.read()
#     server_host = settings.SERVER_HOST
#     link = f"{server_host}/reset-password?token={token}"
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": settings.PROJECT_NAME,
#             "username": email,
#             "email": email_to,
#             "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
#             "link": link,
#         },
#     )


# def send_new_account_email(email_to: str, username: str, password: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - New account for user {username}"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
#         template_str = f.read()
#     link = settings.SERVER_HOST
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": settings.PROJECT_NAME,
#             "username": username,
#             "password": password,
#             "email": email_to,
#             "link": link,
#         },
#     )
