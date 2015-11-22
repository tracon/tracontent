from django.conf import settings
from django.core.cache import caches

import requests


def kompassi_get_programme(event_slug):
    cache = caches['default']
    cache_key = "kompassi_get_programme:{event_slug}".format(event_slug=event_slug)

    cached = cache.get(cache_key)
    if cached:
        return cached

    url = "{kompassi}/events/{event_slug}/programme/fragment".format(
        kompassi=settings.KOMPASSI_HOST,
        event_slug=event_slug,
    )

    response = requests.get(url)
    response.raise_for_status()

    content = response.text

    cache.set(cache_key, content, settings.KOMPASSI_PROGRAMME_EXPIRY_SECONDS)

    return content