from django.urls import path

from prediction.views.admin.get_predictions_by_user import GetPredictionsByUser

urlpatterns = [
    path('retrieve-predictions', GetPredictionsByUser.as_view(), name='get-predictions-by-user'),
]
