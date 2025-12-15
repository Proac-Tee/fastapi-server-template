from fastapi import FastAPI

from src.auth.controller import router as auth_router
from src.users.controller import router as users_router

API_PREFIX = "/api/v1"


def register_routes(app: FastAPI):
    app.include_router(auth_router, prefix=API_PREFIX)
    app.include_router(users_router, prefix=API_PREFIX)
