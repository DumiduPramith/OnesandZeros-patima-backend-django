import json

from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_admin import IsAdmin


class DeleteAccountAdmin(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request):
        user = request.user
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:

            return JsonResponse({'status': 'error', 'message': 'Internal error'}, status=500)
        if user.id == user_id:
            return JsonResponse({"status": "error", "message": "Admin cannot delete own account"}, status=404)
        status = user.delete_account(user_id)
        if status is False:
            return JsonResponse({"status": "error", "message": "Account Deletion Failed"}, status=404)
        elif status is True:
            return JsonResponse({"status": "success", "message": "Account Deleted Successfully"}, status=200)
        return JsonResponse({"status": "error", "message": "Unknown error occured"}, status=404)
