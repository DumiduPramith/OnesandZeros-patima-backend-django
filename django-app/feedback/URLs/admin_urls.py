from django.urls import path

from feedback.views.admin.get_all_feedbacks import GetAllFeedbacks


urlpatterns = [
    path('get-all', GetAllFeedbacks.as_view(), name='get_all_feedbacks'),
]
