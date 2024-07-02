import logging

from patima.utils.database_handler import DatabaseHandler
from users.utils.register_helper import RegisterHelper
from users.utils.login_helper import LoginHelper
from users.utils.forgot_password_helper import ForgotPasswordHelper

class UserExtender(DatabaseHandler, RegisterHelper, LoginHelper, ForgotPasswordHelper):
    def __init__(self, ):
        super().__init__()


class User(UserExtender):
    def __init__(self, email, fname=None, lname=None):
        super().__init__()
        self._id = None
        self._fname = fname
        self._laname = lname
        self._email = email
        self._profile_pic = None
        self._is_authenticated = True
        self._role = 0
        self._role_name = 'User'
        self.logger = logging.getLogger(__name__)

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def fname(self):
        return self._fname

    @property
    def lname(self):
        return self._laname

    @property
    def email(self):
        return self._email

    @property
    def profile_pic(self):
        return self._profile_pic

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @profile_pic.setter
    def profile_pic(self, profile_pic):
        self._profile_pic = profile_pic

    @property
    def role(self):
        return self._role
    
    @property
    def role_name(self):
        return self._role_name

    def register(self, password):
        pass

    def login(self, password):
        login_sql = """
        SELECT u.user_id, u.password, u.activation_status,
           CASE 
               WHEN a.user_id IS NOT NULL THEN 2
               WHEN gp.user_id IS NOT NULL THEN 1
               ELSE 0
           END AS user_role
        FROM user u
        LEFT JOIN archeologist a ON u.user_id = a.user_id
        LEFT JOIN general_public gp ON u.user_id = gp.user_id
        WHERE u.email = %s;
        """
        result = self.run_select_query(login_sql, (self._email,))
        status = self.login_status_maker(result, password)
        if status['Password']:
            self.id = result[0]['user_id']
            self._role = result[0]['user_role']
            self._role_name = 'Archeologist' if self._role == 2 else 'General Public'
        return status

    def delete_account(self, account_id=None):
        sql = 'DELETE FROM user WHERE user_id = %s'
        if account_id is None:
            account_id = (self._id,)
        try:
            affected_no_rows = self.run_delete_query(sql, (account_id,))
        except Exception as e:
            self.logger.error(f"Error deleting account: {e}")
            return False
        if affected_no_rows == 1:
            return True
        return False

    def update_password(self, password):
        from django.contrib.auth.hashers import make_password
        sql = """
        UPDATE user SET password = %s WHERE email = %s
        """
        try:
            password = make_password(password)
            affected_no_rows = self.run_update_query(sql, (password, self._email))
        except Exception as e:
            return False
        if affected_no_rows == 1:
            return True
        return False

    def update_account_details(self, changed_fields):
        if not changed_fields:
            return
        set_clause = ', '.join([f"{key} = %s" for key in changed_fields.keys()])
        values = list(changed_fields.values()) + [self.id]
        query = f"UPDATE user SET {set_clause} WHERE user_id = %s"

        row_count = self.run_update_query(query, values)
        return row_count

    def check_password_match(self, password):
        from django.contrib.auth.hashers import check_password
        sql = 'SELECT password FROM user WHERE user_id = %s'
        result = self.run_select_query(sql, (self._id,))
        return check_password(password, result[0]['password'])
