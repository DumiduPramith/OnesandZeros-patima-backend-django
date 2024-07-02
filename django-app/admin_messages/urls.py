from django.urls import path,include

urlpatterns = [
    path('admin/', include('admin_messages.URLs.admin_urls')),
    path('user/', include('admin_messages.URLs.users_urls')),
]
