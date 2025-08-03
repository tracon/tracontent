from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect


def logout_view(request):
    logout(request)

    next_url = request.GET.get("next", settings.LOGOUT_REDIRECT_URL)
    return redirect(next_url)


def status_view(request):
    return JsonResponse(dict(status="OK"))


ROBOTS_TXT = """
User-agent: *
Allow: /$
Disallow: /
""".strip()


def robots_txt_view(request):
    return HttpResponse(ROBOTS_TXT, content_type="text/plain")
