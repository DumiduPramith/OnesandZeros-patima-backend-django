from django.http import JsonResponse
from rest_framework.views import APIView


class CheckAuthentication(APIView):
    def get(self, request):
        return JsonResponse({'message': 'User is authenticated.'})
