import sys
import logging

from django.conf import settings

import requests
from requests.auth import HTTPBasicAuth



log = logging.getLogger('kompassi_crowd')


class KompassiError(RuntimeError):
    pass


def kompassi_application_auth():
    return HTTPBasicAuth(
        settings.KOMPASSI_API_APPLICATION_NAME,
        settings.KOMPASSI_API_APPLICATION_PASSWORD,
    )


def kompassi_url(*args):
    return u'{base_url}/{path}'.format(
        base_url=settings.KOMPASSI_API_URL,
        path=u'/'.join(unicode(i) for i in args),
    )


KOMPASSI_GET_DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'kompassi_crowd/0.0',
}


def kompassi_get(*args, **kwargs):
    auth = kompassi_application_auth()

    try:
        response = requests.get(
            kompassi_url(*args),
            auth=auth,
            headers=KOMPASSI_GET_DEFAULT_HEADERS,
            params=kwargs,
        )

        response.raise_for_status()

        return response.json()
    except Exception as e:
        log.error(u'Kompassi client GET failed: {e}'.format(e=e))
        unused, unused, traceback = sys.exc_info()
        raise KompassiError, e, traceback


def user_defaults_from_kompassi(kompassi_user):
    return dict((django_key, kompassi_user[kompassi_key]) for (django_key, kompassi_key) in [
        ('username', 'username'),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'surname'),
    ])