from django.urls import path,include
from prediction.views.user.new_predict import Predict
from prediction.views.user.retrieve_user_predictions import RetrieveUserPredictions
from prediction.views.user.get_user_comparisons import GetUserComparisons
from prediction.views.user.get_nearby_predictions import GetNearbyPredictions

urlpatterns = [
    path('new', Predict.as_view(), name="new_predict"),
    path('user/retrieve-predictions', RetrieveUserPredictions.as_view(), name='retrieve_user_predictions'),
    path('user/retrieve-comparisons', GetUserComparisons.as_view(), name='get_user_comparisons'),
    path('user/get-nearby-predictions',GetNearbyPredictions.as_view(),name='get_nearby_predictions'),
    path('admin/', include('prediction.URLs.admin_urls')),
]
