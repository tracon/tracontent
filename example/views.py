from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def public_view(request):
    return render(request, 'index.html')


@login_required
def protected_view(request):
    vars = dict(username=request.user.username)
    return render(request, 'protected.html', vars)
