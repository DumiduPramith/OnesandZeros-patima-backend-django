from django.http.response import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_archeo_general import IsArcheoLogistOrGeneralPub
from prediction.utils.prediction_handler import PredictionHandler


class RetrieveUserPredictions(APIView):
    permission_classes = [IsArcheoLogistOrGeneralPub]

    def get(self, request):
        user_obj = request.user
        prediction_handler = PredictionHandler(user_obj)
        page_number = request.GET.get('page')
        # import time
        # time.sleep(5)
        if page_number is None:
            return JsonResponse({'status': 'error', 'message': 'Page is required'}, status=400)
        try:
            page_number = int(page_number)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Page must be an integer'}, status=400)

        predictions = prediction_handler.retrieve_predictions_by_user_id(page_number)
        if predictions is False:
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=404)
        return JsonResponse({'status': 'success', 'predictions': predictions}, status=200)
