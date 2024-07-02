from .user import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
import logging


class Archeologist(User):
    def __init__(self, email: str = None, fname: str = None, lname: str = None, archeologist_id: int = None):
        super().__init__(email, fname, lname)
        self._archeologist_id = archeologist_id
        self._role = 2
        self._role_name = 'Archeologist'
        self.logger = logging.getLogger(__name__)

    @property
    def archeologist_id(self):
        return self._archeologist_id

    def register(self, password: str):
        try:
            with transaction.atomic():
                query = """
                        INSERT INTO `user` (fname, lname,email,password)
                        VALUES (%s, %s, %s, %s);
                        """
                last_row = self.run_insert_query(query, (self.fname, self.lname, self.email, make_password(password)))
                query2 = """
                        INSERT INTO `archeologist` (user_id, archeologist_id)
                        VALUES (%s, %s);
                        """
                self.run_insert_query(query2, (last_row, self._archeologist_id))
                return True
        except Exception as e:
            self.logger.error(e)
            return False

    def get_account_details(self):
        sql = """
        SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.is_admin,u.activation_status, a.archeologist_id, %s as role
        FROM user u 
        JOIN archeologist a ON u.user_id = a.user_id
        WHERE u.user_id = %s;
        """
        try:
            return self.run_select_query(sql, (self.role,self.id,))
        except Exception as e:
            self.logger.error(f"Error occurred while getting account details: {e}")
            return False

    def get_account_details_for_update(self):
        sql = """
            SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.is_admin,u.activation_status, a.archeologist_id, %s as role
            FROM user u 
            JOIN archeologist a ON u.user_id = a.user_id
            WHERE u.user_id = %s;
        """
        try:
            return self.run_select_query(sql, (self.role,self.id,))
        except Exception as e:
            self.logger.error(f"Error occurred while getting account details: {e}")
            return False

    def change_archeologist_id(self, new_archeologist_id):
        sql = """
        UPDATE archeologist
        SET archeologist_id = %s
        WHERE user_id = %s;
        """
        row_count = self.run_update_query(sql, (new_archeologist_id, self.id))
        return row_count

    def get_all_users(self):
        sql = """
        SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.activation_status, u.is_admin, a.archeologist_id, %s as role
        FROM user u 
        JOIN archeologist a ON u.user_id = a.user_id;
        """
        try:
            result = self.run_select_query(sql,(self.role,))
            return result
        except Exception as e:
            self.logger.error(f"Error occurred while getting all users: {e}")
            return False
