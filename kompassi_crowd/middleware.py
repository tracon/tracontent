import logging

from django.contrib.auth import authenticate, login

from .crowd_client import crowd_validate_session, CrowdError


log = logging.getLogger('kompassi_crowd')


class KompassiCrowdAuthenticationMiddleware(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            try:
                username = crowd_validate_session(request)
            except CrowdError as e:
                log.error(e)
                return None

            if username is not None:
                user = authenticate(username=username) # look, no password

                if user is not None and not user.is_anonymous():
                    login(request, user)

                log.debug("logged in {username} via Crowd".format(username=username))

        return None

