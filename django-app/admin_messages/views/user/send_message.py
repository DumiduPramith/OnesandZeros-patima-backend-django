import json
from django.views import View
from django.http import JsonResponse
import re

from admin_messages.models.message import Message


class SendMessages(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data['email']
            name = data['name']
            message = data['message']
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:

            return JsonResponse({'status': 'error', 'message': 'internal server error'}, status=500)
        email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.([a-zA-Z]{2,}))"
        if not re.match(email_regex, email):
            return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=400)
        status = Message(name, message, email).send_message()
        if status:
            return JsonResponse({'status': 'success', 'message': 'Message saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message not saved'}, status=500)
