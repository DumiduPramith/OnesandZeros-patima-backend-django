import json

from django.http import JsonResponse
from rest_framework.views import APIView

from admin_messages.models.message import Message
from patima.permission.is_admin import IsAdmin


class MarkAsUnRead(APIView):
    # mark message as unread
    permission_classes = [IsAdmin]

    def put(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            message_id = data['message_id']
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'internal server error'}, status=500)
        message_obj = Message()
        status = message_obj.mark_as_un_read(message_id)
        if status:
            return JsonResponse({'status': 'success', 'message': 'Message marked as unread'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message mark as unread failed'}, status=500)
