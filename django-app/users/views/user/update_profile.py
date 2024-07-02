import json
import logging

from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_archeo_general import IsArcheoLogistOrGeneralPub
from users.utils.update_helper import UpdateHelper

logger = logging.getLogger(__name__)


class UpdateOwnProfile(APIView):
    permission_classes = [IsArcheoLogistOrGeneralPub]

    def put(self, request):
        user = request.user
        password_changed = False
        propic_status = False
        if 'json' not in request.POST:
            return JsonResponse({'status': 'success', 'message': 'JSON not found'}, status=400)
        try:
            data = json.loads(request.POST['json'])
            print(data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'success', 'message': 'Invalid JSON'}, status=400)
        if data['profile_picture_changed'] == True:
            try:
                image_file = request.FILES.get('image')
                propic_status = UpdateHelper.save_profile_picture(image_file, user.id)
            except Exception as e:
                logger.error(f'Error occurred: {e}')
                return JsonResponse({'message': 'Internal server error'}, status=500)
        old_data = user.get_account_details_for_update()
        if old_data is None:
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        elif not old_data:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        del data['role']
        changes = UpdateHelper.get_changed_fields(old_data[0], data)
        if propic_status:
            import os
            from django.conf import settings
            img_saved_path = os.path.join("/", settings.PROFILE_PICTURE_SAVING_PATH, str(user.id),
                                          'profile_picture.jpg')
            changes['profile_picture'] = img_saved_path
        if data['password']:
            from django.contrib.auth.hashers import make_password
            is_matched = user.check_password_match(data['old_password'])
            if is_matched is False:
                return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'}, status=400)
            changes['password'] = make_password(data['password'])
            password_changed = True
        if changes == {}:
            return JsonResponse({'status': 'error', 'message': 'No changes detected'}, status=400)
        row_count = user.update_account_details(changes)

        if row_count is False:
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        elif row_count == 0:
            return JsonResponse({'status': 'error', 'message': 'User Not detected'}, status=400)
        return JsonResponse(
            {'status': 'success', 'message': 'Profile updated successfully', 'password_changed': password_changed},
            status=200)
