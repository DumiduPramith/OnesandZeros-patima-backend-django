from django.contrib import admin
from django.urls import path, include
from users.views.confirm_email import ConfirmEmail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('users.URLs.users_urls')),
    path('api/admin/', include('users.URLs.admin_urls')),
    path('confirm-email', ConfirmEmail.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/feedback/', include('feedback.urls')),
    path('api/prediction/', include('prediction.urls')),
    path('api/messages/', include('admin_messages.urls')),
    path('', include('common.urls'))
]
