from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect


def index_view(request):
    return HttpResponse('''
      <h1>Public page</h1>
      <p><a href='/protected'>Go to protected page</a></p>
    ''')


@login_required
def protected_view(request):
    return HttpResponse('<h1>Hello, {user.username}!</h1>'.format(user=request.user))
