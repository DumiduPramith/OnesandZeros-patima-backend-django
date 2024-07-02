import json
from django.views import View
from django.http import JsonResponse
from patima.utils.custom_tokens import CustomRefreshToken
from users.models.user import User
import re

from users.models.admin import Admin


class Login(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email: str = data.get('email')
            password: str = data.get('password')
            role: str = data.get('role')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.([a-zA-Z]{2,}))"
        if not email or not password:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        if not re.match(email_regex, email):
            return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=400)

        if role==3:
            user_obj = Admin(email)
        else:
            user_obj = User(email)
        status = user_obj.login(password)

        if status['User_Not_Found']:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        elif not status['Activation_Status']:
            return JsonResponse({'status': 'error', 'message': 'Email not confirmed'}, status=422)
        elif not status['Password']:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        elif role==3:
            if not status['is_admin']:
                return JsonResponse({'status': 'error', 'message': 'Dont have Permission'}, status=401)
        if status['Role'] is None:
            return JsonResponse({'status': 'error', 'message': 'Unknown error'}, status=500)
        elif status['Password']:
            refresh = CustomRefreshToken.for_user(user_obj)
            return JsonResponse(
                {
                    'status': 'success',
                    'token': {'refresh': str(refresh), 'access': str(refresh.access_token)},
                    'message': f'{user_obj.role_name} logged in successfully',
                    'role': status['Role']
                }
            )
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown error'}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'status': 'error', 'message': 'This method not allowed'}, status=405)
