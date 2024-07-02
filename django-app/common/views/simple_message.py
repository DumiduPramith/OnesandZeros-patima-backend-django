from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class SimpleMessage(View):
    def get(self, request, any_path=None):
        return render(request, '../templates/message.html')
