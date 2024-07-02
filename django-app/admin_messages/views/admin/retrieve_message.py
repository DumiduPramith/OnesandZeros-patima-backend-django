from django.http import JsonResponse
from rest_framework.views import APIView

from admin_messages.models.message import Message
from patima.permission.is_admin import IsAdmin


class RetrieveMessages(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        page = request.GET.get('page')

        if page is None:
            return JsonResponse({'status': 'error', 'message': 'Page is required'}, status=400)
        message_obj = Message()
        messages = message_obj.get_messages(page)
        if messages == False:
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
        return JsonResponse({'status': 'success', 'messages': messages})
