import logging
from pathlib import Path
from typing import Any


def get_logger_settings(LOGS_DIR: Path, DEBUG: bool) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "main_format": {
                "format": (
                    "{asctime} - {levelname} - {filename} - {name} - {message}"
                ),
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console_debug": {
                "format": "{asctime} - \033[1;32m{levelname} "
                "\033[0;35m{module} \033[0;32m{message}\033[0;37m",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console_info": {
                "format": "{asctime} - \033[1;34m{levelname} "
                "\033[0;35m{module} \033[0;34m{message}\033[0;37m",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console_warn": {
                "format": "{asctime} - \033[1;33m{levelname} "
                "\033[0;35m{module} \033[0;33m{message}\033[0;37m",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console_error": {
                "format": "{asctime} - \033[1;31m{levelname} "
                "\033[0;35m{module} \033[0;31m{message}\033[0;37m",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {
            "debug": {
                "()": "django.utils.log.CallbackFilter",
                "callback": lambda record: record.levelno == logging.DEBUG,
            },
            "info": {
                "()": "django.utils.log.CallbackFilter",
                "callback": lambda record: record.levelno == logging.INFO,
            },
            "warning": {
                "()": "django.utils.log.CallbackFilter",
                "callback": lambda record: record.levelno == logging.WARNING,
            },
        },
        "handlers": {
            "console_debug": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "console_debug",
                "filters": ["debug"],
            },
            "console_info": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "console_info",
                "filters": ["info"],
            },
            "console_warn": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "console_warn",
                "filters": ["warning"],
            },
            "console_error": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "console_error",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "main_format",
                "filename": f"{LOGS_DIR}/main.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 10,
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "main_format",
                "filename": f"{LOGS_DIR}/error.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 10,
            },
        },
        "loggers": {
            "main": {
                "handlers": [
                    "file",
                    "console_debug",
                    "console_info",
                    "console_warn",
                    "console_error",
                ],
                "level": "DEBUG" if DEBUG else "INFO",
            },
            "error": {
                "handlers": ["error_file", "console_error"],
                "level": "ERROR",
            },
        },
    }
