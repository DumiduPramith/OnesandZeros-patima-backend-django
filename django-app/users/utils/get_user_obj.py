def get_user_obj(role: int):
    if role == 1:
        from users.models.general_pub import GeneralPub
        return GeneralPub
    elif role == 2:
        from users.models.archeologist import Archeologist
        return Archeologist
    elif role == 3:
        from users.models.admin import Admin
        return Admin
