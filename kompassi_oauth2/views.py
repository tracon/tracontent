from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from django.conf import settings

from requests_oauthlib import OAuth2Session


def get_session(**kwargs):
    return OAuth2Session(settings.KOMPASSI_OAUTH2_CLIENT_ID, **kwargs)


class LoginView(View):
    def get(self, request):
        authorization_url, state = get_session().authorization_url(settings.KOMPASSI_OAUTH2_AUTHORIZE_URL)
        request.session['oauth_state'] = state
        return redirect(authorization_url)


class CallbackView(View):
    def get(self, request):
        session = get_session(state=request.session['oauth_state'])
        token = session.fetch_token(settings.KOMPASSI_OAUTH2_TOKEN_URL,
            client_secret=settings.KOMPASSI_OAUTH2_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri(),
        )

        return redirect(request.GET.get('next', '/'))
