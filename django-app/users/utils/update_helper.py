class UpdateHelper:
    @staticmethod
    def get_changed_fields(existing_fields, new_fields):
        changed_fields = {}
        for key, value in new_fields.items():
            if key in existing_fields and existing_fields[key] != value:
                changed_fields[key] = value
        return changed_fields

    @staticmethod
    def save_profile_picture(image_file,user_id):
        import os
        from django.conf import settings
        if not os.path.exists(settings.PROFILE_PICTURE_SAVING_PATH + str(user_id)):
            os.makedirs(settings.PROFILE_PICTURE_SAVING_PATH + str(user_id))

        img_saved_path = os.path.join(settings.PROFILE_PICTURE_SAVING_PATH, str(user_id), 'profile_picture.jpg')

        with open(img_saved_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        return True