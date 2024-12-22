import logging

from django.apps import AppConfig

from prediction.utils.ml_handler_new import new_run
from prediction.utils.seg_helper import load_segmentation_model

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    segmentation_model = None
    new_generator = None
    prediction_config = {
        'image_size' : 256,
        'padding' : 10,
    }


    def ready(self):
        logger = logging.getLogger(__name__)
        PredictionConfig.new_generator = new_run()
        PredictionConfig.segmentation_model = load_segmentation_model()

