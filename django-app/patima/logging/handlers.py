import os

HANDLERS = {
    "file": {
        "class": "logging.FileHandler",
        "filename": os.getenv("DJANGO_LOG_FILE"),
        "level": os.getenv("DJANGO_LOG_LEVEL"),
        "formatter": "verbose",
    },
    "console": {
        "class": "logging.StreamHandler",
        "level": os.getenv("DJANGO_LOG_LEVEL"),
        "formatter": "verbose"
    }
}
