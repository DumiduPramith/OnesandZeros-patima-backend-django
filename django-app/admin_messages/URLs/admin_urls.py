from django.urls import path

from admin_messages.views.admin.retrieve_message import RetrieveMessages
from admin_messages.views.admin.mark_as_read import MarkAsRead
from admin_messages.views.admin.mark_as_un_read import MarkAsUnRead

urlpatterns = [
    path('retrieve', RetrieveMessages.as_view(), name='submit_feedback'),
    path('mark-as-read', MarkAsRead.as_view(), name='mark_as_read'),
    path('mark-as-unread', MarkAsUnRead.as_view(), name='mark_as_unread'),
]
