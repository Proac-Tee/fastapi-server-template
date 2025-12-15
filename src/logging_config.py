"""
Logging configuration module.

Provides custom log levels and a helper function to configure Python logging.
"""

import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(lineno)d"


class LogLevels(StrEnum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


def configure_logging(log_level: LogLevels = LogLevels.ERROR) -> None:
    """
    Configures Python logging with the specified log level.

    Args:
        log_level (LogLevels): Desired logging level. Defaults to ERROR.
    """
    level = log_level.value.upper()

    log_format = LOG_FORMAT_DEBUG if log_level == LogLevels.DEBUG else None

    if log_format:
        logging.basicConfig(level=level, format=log_format)
    else:
        logging.basicConfig(level=level)
