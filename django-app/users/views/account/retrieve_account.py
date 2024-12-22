from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class RetrieveAccount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        account_details = user.get_account_details()
        if account_details is False:
            return JsonResponse({"status": "error", "message": "No account details found"}, status=404)
        return JsonResponse({"status": "success", "account_details": account_details[0]}, status=200)
