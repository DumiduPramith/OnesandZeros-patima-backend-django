import json
from django.views import View
from django.http import JsonResponse
import re

from users.models.user import User

class ForgotPassword(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Unknown Error'}, status=500)

        email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.([a-zA-Z]{2,}))"
        if not re.match(email_regex, email):
            return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=400)
        user_obj = User(email=email)
        new_password = user_obj.generate_password()
        status = user_obj.update_password(new_password)
        if status is False:
            return JsonResponse({'status': 'error', 'message': 'Error Forgot Password'}, status=500)
        status = user_obj.send_forgot_password_email(new_password)
        if status is False:
            return JsonResponse({'status': 'error', 'message': 'Error Forgot Password'}, status=500)
        return JsonResponse({'status': 'success', 'message': 'Forgot Password Successful. Check your email for new password'})
