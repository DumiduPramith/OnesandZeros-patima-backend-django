import tensorflow as tf
from django.apps import apps

class PredictionHelper:
    @staticmethod
    def _resize(input_image):
        # resize image to 256x256
        HEIGHT = WIDTH = apps.get_app_config('prediction').prediction_config['image_size']
        input_image = tf.image.resize(input_image, [HEIGHT, WIDTH],
                                      method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        return input_image

    @staticmethod
    def _normalize(input_image):
        # normalize image into 0-1
        return (input_image / 127.5) - 1
