from django.urls import path
from feedback.views.user.submit_feedback import SubmitFeedback
from feedback.views.user.get_feedback_user import GetFeedbackUser
from feedback.views.user.feedbacks_by_prediction import FeedbacksByPrediction

urlpatterns = [
    path('submit', SubmitFeedback.as_view(), name='submit feedback'),
    path('feedbacks-all', GetFeedbackUser.as_view(), name='get all feedbacks'),
    path('predicted/all', FeedbacksByPrediction.as_view(), name='get feedbacks by prediction'),
]
