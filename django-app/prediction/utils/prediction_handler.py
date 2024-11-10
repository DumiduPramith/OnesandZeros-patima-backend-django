import logging

from patima.utils.database_handler import DatabaseHandler
from prediction.utils.raw_image_handler import RawImageHandler
from prediction.utils.predicted_image_handler import PredictedImageHandler

class PredictionHandler(RawImageHandler, PredictedImageHandler):
    def __init__(self,usr_obj):
        RawImageHandler.__init__(self,user_obj=usr_obj)
        PredictedImageHandler.__init__(self,user_obj=usr_obj)
        self._usr_obj = usr_obj
        self.logger = logging.getLogger(__name__)

    def admin_retrieve_predictions_by_user_id(self, page_number=1):
        LIMIT = 10
        offset = (page_number - 1) * LIMIT
        sql = """
        SELECT i.image_id, i.input_image_path, i.created_at,i.predicted_image_path,it.tag_name
        FROM image i
        JOIN image_tags it ON it.image_id = i.image_id
        WHERE i.uploader_id = %s
        ORDER BY i.created_at DESC
        LIMIT %s OFFSET %s
        """
        params = (self._user_obj.id, LIMIT, offset)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data[0]['predicted_image_path'] is None:
                data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data
        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return False

    def retrieve_predictions_by_user_id(self, page_number=1):
        LIMIT = 10
        offset = (page_number - 1) * LIMIT
        sql = """
        SELECT i.image_id, i.input_image_path, i.created_at,i.predicted_image_path, it.tag_name
        FROM image i
        JOIN image_tags it ON it.image_id = i.image_id
        WHERE i.uploader_id = %s
        ORDER BY i.created_at DESC
        LIMIT %s OFFSET %s
        """
        params = (self._user_obj.id, LIMIT, offset)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data[0]['predicted_image_path'] is None:
                data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data
        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return False

    def get_predicted_image(self):
        sql = 'SELECT image_id, input_image_path,predicted_image_path,created_at FROM image WHERE image_id = %s '
        params = (self._image_id,)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data:
                if not data[0]['predicted_image_path']:
                    data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data[0]
        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return False

    def save_locations(self,long,lat):
        sql = """
        INSERT INTO image_tags (image_id, tag_name)
        VALUES (%s, CONCAT(%s, ',',%s))
        """
        try:
            DatabaseHandler.run_insert_query(sql, (self._image_id, long,lat))
            return True
        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return False

    def retrieve_nearby_predictions(self, prediction_id, page):
        LIMIT = 10
        OFFSET = (int(page) - 1) * LIMIT

        sql = """
        SELECT i.*
        FROM image_tags it1
        JOIN image_tags it2 ON 6371 * acos(
            cos(radians(SUBSTRING_INDEX(it1.tag_name, ',', 1))) *
            cos(radians(SUBSTRING_INDEX(it2.tag_name, ',', 1))) *
            cos(radians(SUBSTRING_INDEX(it2.tag_name, ',', -1)) - radians(SUBSTRING_INDEX(it1.tag_name, ',', -1))) +
            sin(radians(SUBSTRING_INDEX(it1.tag_name, ',', 1))) *
            sin(radians(SUBSTRING_INDEX(it2.tag_name, ',', 1)))
          ) <= 5
        JOIN image i ON it2.image_id = i.image_id
        WHERE it1.image_id =%s
        LIMIT %s OFFSET %s;
        """
        try:
            data = DatabaseHandler.run_select_query(sql, (prediction_id,LIMIT, OFFSET,))
        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return False
        if data[0]['predicted_image_path'] is None:
            data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
        return data
