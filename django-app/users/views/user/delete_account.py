from django.http import JsonResponse
from rest_framework.views import APIView

from patima.permission.is_archeo_general import IsArcheoLogistOrGeneralPub


class DeleteAccount(APIView):
    permission_classes = [IsArcheoLogistOrGeneralPub]

    def delete(self, request):
        user = request.user
        status = user.delete_account()
        if status is False:
            return JsonResponse({"status": "error", "message": "Account Deletion Failed"}, status=404)
        elif status is True:
            return JsonResponse({"status": "success", "message": "Account Deleted Successfully"}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Unknown error occured"}, status=404)
