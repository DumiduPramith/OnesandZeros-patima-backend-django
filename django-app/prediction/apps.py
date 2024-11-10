import logging

from django.apps import AppConfig
from prediction.utils.ml_handler import run

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    generator = None

    def ready(self):
        logger = logging.getLogger(__name__)
        PredictionConfig.generator = run()
