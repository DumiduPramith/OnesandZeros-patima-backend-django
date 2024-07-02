from django.http import JsonResponse
from rest_framework.views import APIView

from feedback.utils.feedback_handler import FeedbackHandler
from patima.permission.is_admin import IsAdmin


class GetAllFeedbacks(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            page_number = int(request.GET.get('page_number', 1))
        except Exception as e:
            return JsonResponse({"status": "error", 'message': 'Invalid page number'}, status=400)
        feedback_handler = FeedbackHandler(user)
        feedbacks = feedback_handler.get_all_feedbacks(page_number)
        if not feedbacks:
            return JsonResponse({"status": "error", 'message': 'Error occurred while getting feedbacks'}, status=500)
        return JsonResponse({'status': 'success', 'feedbacks': feedbacks})
