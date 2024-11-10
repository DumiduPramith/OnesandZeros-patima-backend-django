import logging

from patima.utils.database_handler import DatabaseHandler
from feedback.models.feedback import Feedback

class FeedbackHandler(DatabaseHandler):
    def __init__(self, user_obj):
        self._user_obj = user_obj
        self.logger = logging.getLogger(__name__)

    def save_feedback(self, feedback_obj):
        query = """
                   INSERT INTO `feedback` (text, rating, image_id, archeologist_user_id)
                   VALUES (%s, %s, %s, %s);
                   """
        try:
            self.run_insert_query(query, (
            feedback_obj.text, feedback_obj.rating, feedback_obj.image_id, self._user_obj.id))
            return True
        except Exception as e:
            self.logger.error(f"Error occurred while saving feedback: {e}")
            return False

    def get_all_feedbacks(self, current_page=1):
        PAGE_SIZE = 10
        try:
            offset = (current_page - 1) * PAGE_SIZE
        except Exception as e:
            self.logger.error(f"Error occurred while getting all feedbacks: {e}")
            return False
        query = f"""
                   SELECT f.feedback_id, f.text, f.rating, f.archeologist_user_id, f.image_id,f.created_at, i.input_image_path,i.predicted_image_path,u.*
                   FROM feedback f
                   JOIN user u ON f.archeologist_user_id = u.user_id
                   JOIN image i ON f.image_id = i.image_id
                   ORDER BY f.feedback_id DESC
                     LIMIT {PAGE_SIZE} OFFSET {offset}
                   """
        try:
            result = self.run_select_query(query)
            if result[0]['predicted_image_path'] is None:
                result[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return result
        except Exception as e:
            self.logger.error(f"Error occurred while getting all feedbacks: {e}")
            return False

    def get_feedbacks_by_user_id(self, user_id):
        query = f"""
                   SELECT f.feedback_id, f.text, f.rating, f.archeologist_user_id, f.image_id,f.created_at,i.input_image_path, i.predicted_image_path
                   FROM feedback f
                   JOIN user u ON f.archeologist_user_id = u.user_id
                   JOIN image i ON f.image_id = i.image_id
                   WHERE f.archeologist_user_id = {user_id}
                    ORDER BY f.feedback_id DESC 
                   """
        try:
            result=  self.run_select_query(query)
            if result[0]['predicted_image_path'] is None:
                result[0]['predicted_image_path'] = '/static/predicted_images/error.png'
        except Exception as e:
            self.logger.error(f"Error occurred while getting feedbacks by user id: {e}")
            return False

    def get_feedbacks_by_predicted_id(self, predicted_id):
        sql = """
        SELECT f.feedback_id, f.text, f.rating, f.archeologist_user_id, f.image_id,f.created_at, i.input_image_path, i.predicted_image_path
        FROM feedback f
        JOIN image i ON f.image_id = i.image_id
        WHERE f.image_id = %s
        """
        try:
            result = self.run_select_query(sql, (predicted_id,))
            if result[0]['predicted_image_path'] is None:
                result[0]['predicted_image_path'] = '/static/predicted_images/error.png'
        except Exception as e:
            self.logger.error(f"Error occurred while getting feedbacks by predicted id: {e}")
            return False
