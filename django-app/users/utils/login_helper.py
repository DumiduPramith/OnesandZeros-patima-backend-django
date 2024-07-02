class LoginHelper:
    def __init__(self):
        self.__token = None
        self.__created = None

    @property
    def login_token(self):
        return self.__token

    @property
    def login_created(self):
        return self.__created

    def login_status_maker(self, result, password):
        from django.contrib.auth.hashers import check_password
        status = {
            'User_Not_Found': True,
            'Activation_Status': False,
            'Password': False,
            'Role': None
        }
        if not result:
            return status
        else:
            status['User_Not_Found'] = False
        if result[0]['activation_status'] == 1:
            status['Activation_Status'] = True
        if result[0]['user_role'] != 0:
            status['Role'] = result[0]['user_role']
        if check_password(password, result[0]['password']):
            status['Password'] = True
            return status
        else:
            return status
