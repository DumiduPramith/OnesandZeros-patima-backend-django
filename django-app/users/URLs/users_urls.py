from django.urls import path

from users.views.login import Login
from users.views.register import Register
from users.views.is_authenticated import CheckAuthentication
from users.views.account.retrieve_account import RetrieveAccount
from users.views.user.delete_account import DeleteAccount
from users.views.forgot_password import ForgotPassword
from users.views.user.update_profile import UpdateOwnProfile

urlpatterns = [
    path('auth/login', Login.as_view()),
    path('auth/register', Register.as_view()),
    path('auth/forgot-password', ForgotPassword.as_view()),
    path('is_authenticated', CheckAuthentication.as_view(), name='is_authenticated'),
    path('retrieve',RetrieveAccount.as_view(), name='retrieve_account'),
    path('user/delete', DeleteAccount.as_view(), name='delete_account'),
    path('user/update', UpdateOwnProfile.as_view(), name='update_profile'),
]
