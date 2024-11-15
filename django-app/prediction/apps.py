import logging

from django.apps import AppConfig
from prediction.utils.ml_handler_step1 import part1_run
from prediction.utils.ml_handler_step2 import part2_run
from prediction.utils.ml_handler import run

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    step1_generator = None
    step2_generator = None
    generator = None


    def ready(self):
        logger = logging.getLogger(__name__)
        PredictionConfig.step1_generator = part1_run()
        PredictionConfig.step2_generator = part2_run()
        # PredictionConfig.generator = run()
