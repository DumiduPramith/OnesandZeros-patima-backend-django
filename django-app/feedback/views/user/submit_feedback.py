import json

from django.http import JsonResponse
from rest_framework.views import APIView

from feedback.models.feedback import Feedback
from feedback.utils.feedback_handler import FeedbackHandler
from patima.permission.is_archeologist import IsArcheologist


class SubmitFeedback(APIView):
    permission_classes = [IsArcheologist]

    def post(self, request):
        # Code to submit feedback
        user = request.user
        try:
            data = json.loads(request.body.decode('utf-8'))
            rating = data.get('rating')
            question1 = data.get('question1')
            question2 = data.get('question2')
            question3 = data.get('question3')
            feedback = data.get('feedback')
            image_id = data.get('image_id')

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

        text = f"{question1}|{question2}|{question3}|{feedback}"

        feedback_obj = Feedback(text, rating, image_id)
        if not feedback_obj.is_valid():
            return JsonResponse({'message': 'Invalid data'}, status=400)
        feedback_handler_obj = FeedbackHandler(user)
        if not feedback_handler_obj.save_feedback(feedback_obj):
            return JsonResponse({'message': 'Error occurred while saving feedback'}, status=500)

        return JsonResponse({'message': 'Feedback saved successfully'}, status=200)
