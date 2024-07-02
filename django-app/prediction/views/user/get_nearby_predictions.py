from django.http.response import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_archeo_general import IsArcheoLogistOrGeneralPub
from prediction.utils.prediction_handler import PredictionHandler


class GetNearbyPredictions(APIView):
    permission_classes = [IsArcheoLogistOrGeneralPub]

    def get(self, request):
        user_obj = request.user
        prediction_id = request.GET.get('pred_id', 1)
        page = 1
        try:
            prediction_id = int(prediction_id)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid prediction id'}, status=400)
        prediction_handler = PredictionHandler(user_obj)
        data = prediction_handler.retrieve_nearby_predictions(prediction_id, page)
        if data:
            return JsonResponse({'status': 'success', 'predictions': data}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Error occurred while fetching data'}, status=500)
