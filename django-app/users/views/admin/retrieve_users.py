import logging

from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_admin import IsAdmin
from users.utils.get_user_obj import get_user_obj


class RetrieveUsers(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        try:
            role = request.GET.get('role')
        except Exception as e:
            logging.error('Error in RetrieveUsers.get: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        if role is None:
            return JsonResponse({'status': 'error', 'message': 'Role is required'}, status=400)
        try:
            user_obj = get_user_obj(int(role))()
        except Exception as e:
            logging.error('Error in RetrieveUsers.get: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        users_list = user_obj.get_all_users()
        if users_list is False:
            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)

        return JsonResponse({'status': 'success', 'users': users_list}, status=200)
