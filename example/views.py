from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, redirect


def public_view(request):
    return render(request, 'index.html')


@login_required
def protected_view(request):
    vars = dict(username=request.user.username)
    return render(request, 'protected.html', vars)


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_URL)