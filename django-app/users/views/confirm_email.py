from django.views import View
from django.shortcuts import redirect
from django.contrib import messages


class ConfirmEmail(View):
    def get(self, request):
        signed_email = request.GET.get('link')
        if not signed_email:
            messages.error(request, 'Invalid link')
            return redirect('confirm-email/error')
        from django.core import signing
        signer = signing.Signer()
        try:
            email = signer.unsign(signed_email)
        except signing.BadSignature:
            messages.error(request, 'Invalid link')
            return redirect('confirm-email/error')
        from ..models.user import User
        user = User(email)
        if user.confirm_email_update():
            messages.success(request, 'Email confirmed Successfully')
            return redirect('confirm-email/success')
        else:
            messages.error(request, 'Email confirmation failed')
            return redirect('confirm-email/error')

    def HttpResponseNotAllowed(self, request, *args, **kwargs):
        messages.error(request, 'error')
        return redirect('confirm-email/error')
