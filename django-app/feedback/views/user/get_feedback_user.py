from django.http import JsonResponse
from rest_framework.views import APIView

from feedback.utils.feedback_handler import FeedbackHandler
from patima.permission.is_archeologist import IsArcheologist


class GetFeedbackUser(APIView):
    # retrieve all feedbacks user submitted
    permission_classes = [IsArcheologist]

    def get(self, request):
        # Code to get feedback
        user = request.user
        feedback_handler = FeedbackHandler(user)
        feedbacks = feedback_handler.get_feedbacks_by_user_id(user.id)
        if not feedbacks:
            return JsonResponse({'message': 'No feedbacks found'}, status=404)

        for feedback in feedbacks:
            decoded_question1, decoded_question2, decoded_question3, decoded_user_provided_feedback = feedback[
                'text'].split('|')
            del feedback['text']
            feedback['question1'] = decoded_question1
            feedback['question2'] = decoded_question2
            feedback['question3'] = decoded_question3
            feedback['feedback'] = decoded_user_provided_feedback
        return JsonResponse({'massage': 'success', 'feedbacks': feedbacks}, status=200)
