from django.http import JsonResponse
from rest_framework.views import APIView

from feedback.utils.feedback_handler import FeedbackHandler
from patima.permission.is_archeologist import IsArcheologist


class FeedbacksByPrediction(APIView):
    permission_classes = [IsArcheologist]

    def get(self, request):
        # Code to get feedback
        user = request.user
        predicted_id = request.GET.get('pred_id')
        if predicted_id is None:
            return JsonResponse({'status': 'error', 'message': 'Predicted ID is required'}, status=400)
        try:
            predicted_id = int(predicted_id)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Predicted ID must be an integer'}, status=400)
        feedback_handler = FeedbackHandler(user)
        feedbacks = feedback_handler.get_feedbacks_by_predicted_id(predicted_id)
        if not feedbacks:
            return JsonResponse({'status': 'error', 'message': 'No feedbacks found'}, status=404)
        for feedback in feedbacks:
            decoded_question1, decoded_question2, decoded_question3, decoded_user_provided_feedback = feedback[
                'text'].split('|')
            del feedback['text']
            feedback['question1'] = decoded_question1
            feedback['question2'] = decoded_question2
            feedback['question3'] = decoded_question3
            feedback['feedback'] = decoded_user_provided_feedback

        return JsonResponse({'status': 'success', 'feedbacks': feedbacks}, status=200)
