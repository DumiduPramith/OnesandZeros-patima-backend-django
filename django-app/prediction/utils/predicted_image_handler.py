from django.conf import settings
from PIL import Image
import logging
import os
import tensorflow as tf

from patima.utils.database_handler import DatabaseHandler

logger = logging.getLogger(__name__)

class PredictedImageHandler:
    def __init__(self, user_obj):
        self._user_obj = user_obj
        self._image_extension = '.jpg'
        self._img_saved_path = None
        self._processed = False

    def save_predicted_image_db(self):
        # save predicted image save location in db
        if not self._processed:
            return False
        sql = '''UPDATE image SET predicted_image_path=%s
               WHERE image_id=%s
               '''
        img_path = os.path.join("/", settings.PREDICTED_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                (str(self.image_id) + self._image_extension))
        lastrow_id = DatabaseHandler.run_insert_query(sql, (img_path, self.image_id))
        return lastrow_id is not None

    def save_predicted_image_file(self, predicted_image):
        # save predicted image in file system
        if not os.path.exists(settings.PREDICTED_IMAGE_SAVING_PATH + str(self._user_obj.id)):
            os.makedirs(settings.PREDICTED_IMAGE_SAVING_PATH + str(self._user_obj.id))

        self._img_saved_path = os.path.join(settings.PREDICTED_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                            (str(self.image_id) + self._image_extension))
        predicted_image = (predicted_image * 255).numpy().astype('uint8')

        encoded_image = tf.image.encode_jpeg(predicted_image, quality=95)
        try:
            tf.io.write_file(self._img_saved_path, encoded_image)
            self._processed = True
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False
        return True

