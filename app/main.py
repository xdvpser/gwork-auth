from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import router
from app.db.session import database
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/auth/openapi.json",
    docs_url="/api/auth/docs",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix="/api/auth")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
