from fastapi import FastAPI

from src.api import register_routes
from src.logging_config import LogLevels, configure_logging
from src.settings import settings

configure_logging(LogLevels.INFO)


app = FastAPI(
    docs_url=None if settings.APP_ENV == "production" else "/docs",
    redoc_url=None if settings.APP_ENV == "production" else "/redoc",
    openapi_url=None if settings.APP_ENV == "production" else "/openapi.json",
)
register_routes(app)
