import json
import logging
import sys
from datetime import datetime

from django.conf import settings

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth


log = logging.getLogger('kompassi_crowd')


class CrowdError(RuntimeError):
    pass


def crowd_application_auth():
    return HTTPBasicAuth(
        settings.KOMPASSI_CROWD_APPLICATION_NAME,
        settings.KOMPASSI_CROWD_APPLICATION_PASSWORD
    )


def crowd_session_url(token=None):
    base_url = settings.KOMPASSI_CROWD_SESSION_URL

    if token is not None:
        return "{base_url}/{token}".format(base_url=base_url, token=token) # TODO validate token?
    else:
        return base_url


def crowd_get_logged_in_user(request, token):
    if token is None:
        return None

    headers = {
        'Accept': 'application/json',
    }

    try:
        response = requests.get(
            crowd_session_url(token),
            auth=crowd_application_auth(),
            headers=headers,
        )

        response.raise_for_status()

        response_json = response.json()

        return response_json['username']
    except Exception as e:
        log.error(u'Crowd session fetching failed: {e}'.format(e=e))
        unused, unused, traceback = sys.exc_info()
        raise CrowdError, e, traceback


def crowd_refresh_session(token, username):
    """
    Validates a Crowd SSO session for the specified user.
    """

    validation_factors = []

    for vf_name, vf_func in settings.KOMPASSI_CROWD_VALIDATION_FACTORS.iteritems():
        validation_factors.append(dict(
            name=vf_name,
            value=vf_func(request),
        ))

    auth = crowd_application_auth()

    # https://developer.atlassian.com/display/CROWDDEV/JSON+Requests+and+Responses
    # https://developer.atlassian.com/display/CROWDDEV/Crowd+REST+Resources#CrowdRESTResources-CrowdSSOTokenResource

    params = {'validate-password': 'false'}

    payload = {
        'username': username,
        'validation-factors': {
            'validationFactors': validation_factors
        },
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    log.debug(
        u'Refreshing Crowd SSO session for {username} validation factors: {validation_factors}'
        .format(
            username=username,
            validation_factors=validation_factors,
        )
    )

    try:
        response = requests.post(
            crowd_session_url(token),
            auth=auth,
            data=json.dumps(payload),
            headers=headers,
            params=params,
        )

        response.raise_for_status()
    except Exception as e:
        log.error(u'Crowd authentication failed for {username}: {e}'.format(username=username, e=e))
        unused, unused, traceback = sys.exc_info()
        raise CrowdError, e, traceback

    log.debug(u'Crowd session refresh succeeded for {username}'.format(username=username))


def crowd_validate_session(request):
    token = request.COOKIES.get(settings.KOMPASSI_CROWD_COOKIE_NAME, None)

    if token is None:
        return None

    username = crowd_get_logged_in_user(token)

    if username is None:
        return None

    try:
        crowd_refresh_session(token, username)
    except CrowdError as e:
        log.error(u'Failed to validate session: {e}'.format(e=e))
        return None

    return username
