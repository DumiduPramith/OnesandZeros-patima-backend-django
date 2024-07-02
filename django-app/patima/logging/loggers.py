import os

LOGGERS = {
    "": {
        "level": os.getenv("DJANGO_LOG_LEVEL"),
        "handlers": ["file", "console"],
    }
}
