from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)

    next_url = request.GET.get('next', settings.LOGOUT_REDIRECT_URL)
    return redirect(next_url)