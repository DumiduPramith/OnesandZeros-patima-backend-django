import logging

from .user import User


class Admin(User):
    def __init__(self, email=None):
        super().__init__(email)
        self._role = 3
        self._role_name = 'Admin'
        self.logger = logging.getLogger(__name__)

    @property
    def role(self):
        return self._role

    @property
    def role_name(self):
        return self._role_name

    def login(self, password: str):
        query = """
                SELECT user.user_id,password,activation_status, is_admin FROM `user` 
                WHERE email = %s;
                        """
        result = self.run_select_query(query, (self.email,))
        if result:
            result[0]['user_role'] = 3
        status = self.login_status_maker(result, password)
        if result:
            if result[0]['is_admin']:
                status['is_admin'] = True
            else:
                status['is_admin'] = False
        if status['Password']:
            self.id = result[0]['user_id']
        return status

    def get_all_users(self):
        sql = """
        SELECT u.user_id, u.email, u.fname, u.lname, u.profile_picture, u.activation_status, u.is_admin, u.activation_status,
            CASE 
               WHEN a.user_id IS NOT NULL THEN 2
               WHEN gp.user_id IS NOT NULL THEN 1
               ELSE 0
            END AS role
        FROM user u
        LEFT JOIN archeologist a ON u.user_id = a.user_id
        LEFT JOIN general_public gp ON u.user_id = gp.user_id
        WHERE u.is_admin = 1;
        """
        try:
            result = self.run_select_query(sql)
            return result
        except Exception as e:
            return False
