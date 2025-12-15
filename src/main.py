from fastapi import FastAPI

from src.api import register_routes
from src.logging_config import LogLevels, configure_logging

configure_logging(LogLevels.INFO)

app = FastAPI()

register_routes(app)
