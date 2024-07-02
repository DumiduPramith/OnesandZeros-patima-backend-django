from users.models.user import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
import logging


class GeneralPub(User):
    # General public role = 1
    def __init__(self, email: str = None, fname: str = None, lname: str = None, *args, **kwargs):
        super().__init__(email, fname, lname)
        self._role = 1
        self._role_name = 'General Public'
        self.logger = logging.getLogger(__name__)

    def register(self, password):
        try:
            with transaction.atomic():
                query = """
                        INSERT INTO `user` (fname, lname,email,password)
                        VALUES (%s, %s, %s, %s);
                        """
                last_row = self.run_insert_query(query, (self.fname, self.lname, self.email, make_password(password)))
                query2 = """
                        INSERT INTO `general_public` (user_id)
                        VALUES (%s);
                        """
                self.run_insert_query(query2, (last_row,))
                return True
        except Exception as e:
            return False

    def get_account_details(self):
        sql = """
        SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.is_admin, %s as role
        FROM user u
        WHERE u.user_id = %s;
        """
        try:
            return self.run_select_query(sql, (self.role,self.id,))
        except Exception as e:
            self.logger.error(f"Error occurred while getting account details: {e}")
            return False


    def get_account_details_for_update(self):
        sql = """
                SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.is_admin, %s as role, u.activation_status
                FROM user u
                WHERE u.user_id = %s;
                """
        try:
            return self.run_select_query(sql, (self.role, self.id,))
        except Exception as e:
            self.logger.error(f"Error occurred while getting account details: {e}")
            return False


    def get_all_users(self):
        sql = """
        SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.activation_status, u.is_admin, u.activation_status, %s as role
        FROM user u
        JOIN general_public a ON u.user_id = a.user_id;
        """
        try:
            result = self.run_select_query(sql, (self.role,))
            return result
        except Exception as e:
            return False