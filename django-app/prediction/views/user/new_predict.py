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
            return JsonResponse({'status': 'success', 'message': 'Image not found'}, status=400)
        else:
            prediction_handler = PredictionHandler(user_obj)
            if not prediction_handler.save_image(image_file):
                return JsonResponse({'status': 'success', 'message': 'Error occurred while saving image'}, status=500)
            status = prediction_handler.save_db()
            if status:
                result = prediction_handler.predict(image_file)
            longitude = json_data['longitude']
            latitude = json_data['latitude']
            status1 = prediction_handler.save_locations(longitude, latitude)
            if status1 is False:
                return JsonResponse({'status': 'error', 'message': 'Error occurred while saving locations'}, status=500)
            if status:
                result = prediction_handler.get_predicted_image()
                return JsonResponse({'status': 'success', 'prediction': result}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Error occurred while saving image'}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success', 'message': 'Method not allowed'}, status=405)
