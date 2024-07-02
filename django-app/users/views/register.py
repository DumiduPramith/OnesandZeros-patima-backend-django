import json

from django.views import View
from django.http import JsonResponse
import re

from users.utils.get_user_obj import get_user_obj


class Register(View):
    def post(self, request):
        from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request)
        try:
            data = json.loads((request.body.decode('utf-8')))
            fname: str = data.get('fname')
            lname: str = data.get('lname')
            email: str = data.get('email')
            password: str = data.get('password')
            role = data.get('role')
            archeologist_id = data.get('archeologist_id')

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.([a-zA-Z]{2,}))"
        if not re.match(email_regex, email):
            return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=400)
        elif role == 2 and not archeologist_id:
            return JsonResponse({'status': 'error', 'message': 'Archelogist ID is required'}, status=400)
        elif role in (1, 3) and archeologist_id:
            return JsonResponse({'status': 'error', 'message': 'Archelogist ID is not required for this role'},
                                status=400)
        elif role > 3 or role < 1:
            return JsonResponse({'status': 'error', 'message': 'Invalid role'}, status=400)

        user = get_user_obj(role)
        user_obj = user(email, fname, lname, archeologist_id)
        if user_obj.email_already_exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'}, status=409)
        status = user_obj.register(password)
        if status:
            status = user_obj.send_conf_email(current_site)
        else:
            return JsonResponse({'status': 'error', 'message': f'Error registering {user_obj.role_name}'}, status=500)
        if status:
            return JsonResponse({'status': 'success', 'message': f'{user_obj.role_name} registered successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error Sending Activation Email'}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'status': 'error', 'message': 'This method not allowed'}, status=405)
