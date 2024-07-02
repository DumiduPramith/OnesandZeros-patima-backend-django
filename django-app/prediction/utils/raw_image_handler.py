import os
import logging
from patima.utils.database_handler import DatabaseHandler
from django.conf import settings

logger = logging.getLogger(__name__)

class RawImageHandler:
    def __init__(self, user_obj):
        self._user_obj = user_obj
        self._processed = False
        self._image_extension = '.jpg'
        self._img_saved_path = None
        self._image_id = None

    @property
    def image_id(self):
        return self._image_id

    def save_db(self):
        if not self._processed:
            return False
        sql = 'INSERT INTO image (input_image_path, uploader_id) VALUES (%s, %s)'
        img_path = os.path.join("/",settings.RAW_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                (str(self._get_next_image_id()) + self._image_extension))
        lastrow_id = DatabaseHandler.run_insert_query(sql, (img_path, self._user_obj.id))
        self._image_id = lastrow_id
        return lastrow_id is not None

    def save_image(self, image_file):
        # save image in file system
        if not os.path.exists(settings.RAW_IMAGE_SAVING_PATH + str(self._user_obj.id)):
            os.makedirs(settings.RAW_IMAGE_SAVING_PATH + str(self._user_obj.id))

        image_id = self._get_next_image_id()
        self._img_saved_path = os.path.join(settings.RAW_IMAGE_SAVING_PATH, str(self._user_obj.id),
                                            (str(image_id) + self._image_extension))
        try:
            with open(self._img_saved_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            self._processed = True
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False
        return True

    @staticmethod
    def _get_next_image_id():
        sql = 'SELECT MAX(image_id) FROM image'
        max_id = DatabaseHandler.run_select_query(sql)
        return max_id[0]['MAX(image_id)'] + 1 if max_id[0]['MAX(image_id)'] else 1
