from django.urls import path,include

urlpatterns = [
    path('admin/', include('feedback.URLs.admin_urls')),
    path('user/', include('feedback.URLs.users_urls')),
]
