import json
import logging

from django.http.response import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_archeo_general import IsArcheoLogistOrGeneralPub
from prediction.utils.prediction_handler import PredictionHandler

logger = logging.getLogger(__name__)


class Predict(APIView):
    permission_classes = [IsArcheoLogistOrGeneralPub]

    def post(self, request):
        # Code to predict
        user_obj = request.user
        if 'json' not in request.POST:
            return JsonResponse({'status': 'error', 'message': 'JSON not found'}, status=400)
        try:
            json_data = json.loads(request.POST['json'])
            print(json_data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        try:
            image_file = request.FILES.get('image')
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return JsonResponse({'message': 'Internal server error'}, status=500)
        if not image_file:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=400)
        else:
            predictionHandler = PredictionHandler(user_obj)
            if not predictionHandler.save_raw_image_file(image_file):
                return JsonResponse({'status': 'error', 'message': 'Error occurred while saving image'}, status=500)
            status = predictionHandler.save_raw_image_db()
            if status:
                predicted_image = predictionHandler.predict(image_file)
                status = predictionHandler.save_predicted_image_file(predicted_image)
                if status:
                    status = predictionHandler.save_predicted_image_db()
            longitude = json_data['longitude']
            latitude = json_data['latitude']
            status1 = predictionHandler.save_locations(longitude, latitude)
            if status1 is False:
                return JsonResponse({'status': 'error', 'message': 'Error occurred while saving locations'}, status=500)
            if status:
                result = predictionHandler.get_predicted_image()
                return JsonResponse({'status': 'success', 'prediction': result}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Error occurred while saving image'}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success', 'message': 'Method not allowed'}, status=405)
