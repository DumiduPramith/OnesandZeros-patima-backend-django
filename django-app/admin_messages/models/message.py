import logging
from patima.utils.database_handler import DatabaseHandler

class Message(DatabaseHandler):
    def __init__(self, name=None, message=None, email=None):
        self._name = name
        self._message = message
        self._email = email
        self.logger = logging.getLogger(__name__)

    def send_message(self):
        query = """
        INSERT INTO admin_messages (name, message_text, email)
        VALUES (%s, %s, %s)
        """
        try:
            self.run_insert_query(query, (self._name, self._message, self._email))
        except Exception as e:
            self.logger.error(f"Error sending message: {str(e)}")
            return False
        return True

    def get_messages(self, page):
        LIMIT = 10
        OFFSET = (int(page)-1) * LIMIT

        query = """
        SELECT * FROM admin_messages
        LIMIT %s OFFSET %s
        """
        try:
            result = self.run_select_query(query, (LIMIT, OFFSET,))
        except Exception as e:
            self.logger.error(f"Error getting messages: {str(e)}")
            return False
        return result


    def mark_as_read(self, message_id):
        query = """
        UPDATE admin_messages
        SET check_status = 1
        WHERE message_id = %s
        """
        try:
            affected_rows = self.run_update_query(query, (message_id,))
        except Exception as e:
            self.logger.error(f"Error marking message as read: {str(e)}")
            return False
        if affected_rows == 0:
            return False
        return True

    def mark_as_un_read(self, message_id):
        query = """
        UPDATE admin_messages
        SET check_status = 0
        WHERE message_id = %s
        """
        try:
            affected_rows = self.run_update_query(query, (message_id,))
        except Exception as e:
            self.logger.error(f"Error marking message as not read: {str(e)}")
            return False
        if affected_rows == 0:
            return False
        return True
