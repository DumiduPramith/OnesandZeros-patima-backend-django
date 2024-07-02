from django.urls import path

from admin_messages.views.user.send_message import SendMessages

urlpatterns = [
    path('send', SendMessages.as_view(), name='send messages'),
]
