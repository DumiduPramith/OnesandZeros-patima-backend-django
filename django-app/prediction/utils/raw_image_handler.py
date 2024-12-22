import os
import logging
import tensorflow as tf
from django.conf import settings

from patima.utils.database_handler import DatabaseHandler
from prediction.utils.helper import PredictionHelper

logger = logging.getLogger(__name__)

class RawImageHandler(PredictionHelper):
    def __init__(self, user_obj):
        self._user_obj = user_obj
        self._processed = False
        self._image_extension = '.jpg'
        self._img_saved_path = None
        self._image_id = None

    @property
    def image_id(self):
        return self._image_id

    def save_raw_image_db(self):
        # save user input raw image save location in db
        if not self._processed:
            return False
        sql = 'INSERT INTO image (input_image_path, uploader_id) VALUES (%s, %s)'
        img_path = os.path.join("/",settings.RAW_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                (str(self._get_next_image_id()) + self._image_extension))
        lastrow_id = DatabaseHandler.run_insert_query(sql, (img_path, self._user_obj.id))
        self._image_id = lastrow_id
        return lastrow_id is not None

    def save_raw_image_file(self, image_file):
        # save image in file system
        if not os.path.exists(settings.RAW_IMAGE_SAVING_PATH + str(self._user_obj.id)):
            os.makedirs(settings.RAW_IMAGE_SAVING_PATH + str(self._user_obj.id))

        image_id = self._get_next_image_id()
        self._img_saved_path = os.path.join(settings.RAW_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                            (str(image_id) + self._image_extension))
        image_bytes = b''.join(image_file.chunks())
        input_images = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)

        # Resize image
        resized_image = self._resize(input_images)
        resized_image_bytes = tf.io.encode_jpeg(resized_image).numpy()
        with open(self._img_saved_path, 'wb+') as destination:
            destination.write(resized_image_bytes)
        self._processed = True

        return True

    @staticmethod
    def _get_next_image_id():
        # return next image saving number (id)
        sql = 'SELECT MAX(image_id) FROM image'
        max_id = DatabaseHandler.run_select_query(sql)
        return max_id[0]['MAX(image_id)'] + 1 if max_id[0]['MAX(image_id)'] else 1
