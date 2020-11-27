from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import path, re_path


def logout_view(request):
    logout(request)

    next_url = request.GET.get('next', settings.LOGOUT_REDIRECT_URL)
    return redirect(next_url)


def status_view(request):
    return JsonResponse(dict(status='OK'))
