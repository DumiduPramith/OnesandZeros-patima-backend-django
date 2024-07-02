from django.urls import path

from users.views.admin.delete_account import DeleteAccountAdmin
from users.views.admin.retrieve_users import RetrieveUsers
from users.views.admin.update_profile import UpdateProfile

urlpatterns = [
    path('retrieve-users', RetrieveUsers.as_view(), name='retrieve_accounts'),
    path('delete-user', DeleteAccountAdmin.as_view(), name='delete_account_from_admin'),
    path('update-user', UpdateProfile.as_view(), name='update_user'),
]
