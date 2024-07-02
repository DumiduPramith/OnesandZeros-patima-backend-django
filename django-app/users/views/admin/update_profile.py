import json
import logging

from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_admin import IsAdmin
from users.utils.get_user_obj import get_user_obj
from users.utils.update_helper import UpdateHelper


class UpdateProfile(APIView):
    permission_classes = [IsAdmin]

    def put(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            role = data.get('role')
            user_id = data.get('user_id')
        except json.JSONDecodeError:
            logging.error('Error in RetrieveUsers.put: Invalid JSON')
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logging.error('Error in RetrieveUsers.put: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)

        if role is None:
            return JsonResponse({'status': 'error', 'message': 'Role is required'}, status=400)

        user_obj = get_user_obj(int(role))()
        user_obj.id = user_id
        del data['role']
        old_data = user_obj.get_account_details_for_update()

        if old_data is None:
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        elif not old_data:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        changes = UpdateHelper.get_changed_fields(old_data[0], data)
        if data['password']:
            from django.contrib.auth.hashers import make_password
            changes['password'] = make_password(data['password'])
        if changes == {}:
            return JsonResponse({'status': 'error', 'message': 'No changes detected'}, status=400)
        try:
            with transaction.atomic():
                if 'archeologist_id' in changes:
                    archeologist_id = changes.pop('archeologist_id')
                    archeologist_row_count = user_obj.change_archeologist_id(archeologist_id)
                    if archeologist_row_count == 0:
                        raise Exception('Archeologist not found')
                    elif archeologist_row_count > 1:
                        raise Exception('Multiple archeologists found')

                if changes != {}:
                    row_count = user_obj.update_account_details(changes)
        except Exception as e:
            logging.error('Error in UpdateProfile.put: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        if row_count is False:
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        elif row_count == 0:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        elif row_count > 1:
            return JsonResponse({'status': 'error', 'message': 'Multiple users found'}, status=500)
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'}, status=200)
