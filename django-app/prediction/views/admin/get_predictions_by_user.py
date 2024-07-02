from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_admin import IsAdmin
from prediction.utils.prediction_handler import PredictionHandler


class GetPredictionsByUser(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            page_number = int(request.GET.get('page_number', 1))
            user_id = int(request.GET.get('user_id', 1))
            user.id = user_id
        except Exception as e:
            return JsonResponse({"status": "error", 'message': 'Invalid page number'}, status=400)
        prediction_obj = PredictionHandler(user)
        predictions = prediction_obj.admin_retrieve_predictions_by_user_id(page_number)
        if not predictions:
            return JsonResponse({"status": "error", 'message': 'Error occurred while getting predictions'}, status=500)
        return JsonResponse({'status': 'success', 'predictions': predictions})
