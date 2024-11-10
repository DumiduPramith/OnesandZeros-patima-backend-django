from django.apps import apps
from django.conf import settings
import tensorflow as tf
from PIL import Image
import os
import logging

from patima.utils.database_handler import DatabaseHandler

if os.getenv('DJANGO_ENV') == 'dev':
    from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

class PredictedImageHandler:
    def __init__(self, user_obj):
        self._user_obj = user_obj
        self._image_extension = '.jpg'
        self._img_saved_path = None
        self._processed = False
        self.generator = apps.get_app_config('prediction').generator

    def _save_db(self):
        if not self._processed:
            return False
        sql = '''UPDATE image SET predicted_image_path=%s
               WHERE image_id=%s
               '''
        img_path = os.path.join("/", settings.PREDICTED_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                (str(self.image_id) + self._image_extension))
        lastrow_id = DatabaseHandler.run_insert_query(sql, (img_path, self.image_id))
        return lastrow_id is not None

    def _save_image(self, predicted_image):
        # save image in file system
        if not os.path.exists(settings.PREDICTED_IMAGE_SAVING_PATH + str(self._user_obj.id)):
            os.makedirs(settings.PREDICTED_IMAGE_SAVING_PATH + str(self._user_obj.id))

        self._img_saved_path = os.path.join(settings.PREDICTED_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                            (str(self.image_id) + self._image_extension))
        if len(predicted_image.shape) == 4:
            predicted_image = tf.squeeze(predicted_image, axis=0)

        predicted_image = (predicted_image * 0.5) + 0.5

        predicted_image = tf.clip_by_value(predicted_image, 0,1)
        predicted_image = (predicted_image * 255).numpy().astype('uint8')

        predicted_image = Image.fromarray(predicted_image)
        try:
            predicted_image.save(self._img_saved_path)
            self._processed = True
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False
        return True

    @staticmethod
    def _resize(input_image):
        HEIGHT= WIDTH = 256
        input_image = tf.image.resize(input_image, [HEIGHT, WIDTH],
                                      method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        return input_image

    @staticmethod
    def _normalize(input_image):
        return (input_image / 127.5) - 1

    def predict(self, input_image):
        input_image.seek(0)
        image_bytes = input_image.read()
        try:
            input_image = tf.io.decode_image(image_bytes, channels=3)
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False
        input_image = tf.cast(input_image, tf.float32)
        input_image = self._resize(input_image)
        input_image = self._normalize(input_image)
        input_image = tf.expand_dims(input_image, 0)

        generated_image = self.generator(input_image, training=False)
        if os.getenv('DJANGO_ENV') == 'dev':
            plt.subplot(1, 2, 1)
            plt.imshow(generated_image[0] * 0.5 + 0.5)
            plt.subplot(1, 2, 2)
            plt.imshow(input_image[0] * 0.5 + 0.5)
            plt.show()

        status = self._save_image(generated_image)
        if status:
            return self._save_db()
