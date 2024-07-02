from django.urls import path
from common.views.simple_message import SimpleMessage


urlpatterns = [
    path('<str:any_path>/success',SimpleMessage.as_view()),
    path('<str:any_path>/error',SimpleMessage.as_view())
]