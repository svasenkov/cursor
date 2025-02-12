import logging.config
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": settings.LOG_FORMAT
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": settings.LOG_LEVEL
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "app.log",
                "maxBytes": 1024 * 1024,  # 1MB
                "backupCount": 5,
                "level": settings.LOG_LEVEL
            }
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console", "file"]
        }
    }
    logging.config.dictConfig(logging_config) 