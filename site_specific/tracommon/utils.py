import re

from django.conf import settings
from django.core.cache import caches

import requests


def kompassi_get_programme(event_slug, special=False, category=None):
    cache = caches['default']
    cache_key = f"kompassi_get_programme:{event_slug}"

    cached = cache.get(cache_key)
    if cached:
        return cached

    url = "{kompassi}/events/{event_slug}/programme/{special}fragment{query}".format(
        kompassi=settings.KOMPASSI_HOST,
        event_slug=event_slug,
        special='special/' if special else '',
        query='?category={category}'.format(category=category) if category else '',
    )

    response = requests.get(url)
    response.raise_for_status()

    content = response.text

    cache.set(cache_key, content, settings.KOMPASSI_PROGRAMME_EXPIRY_SECONDS)

    return content


def kompassi_get_teams(event_slug):
    cache = caches['default']
    cache_key = f"kompassi_get_teams:{event_slug}"

    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{settings.KOMPASSI_HOST}/api/v1/events/{event_slug}/teams"

    response = requests.get(url)
    response.raise_for_status()

    content = response.json()['teams']

    cache.set(cache_key, content, settings.KOMPASSI_PROGRAMME_EXPIRY_SECONDS)

    return content


DOMAIN_REGEXEN = [
    re.compile(r'^(?P<year>\d+)\.(?P<event>tracon)\.fi$'),
    re.compile(r'^(?P<year>\d+)\.(?P<event>hitpoint)\.tracon.fi$'),
]

def event_slug_from_domain(domain):
    for regex in DOMAIN_REGEXEN:
        match = regex.match(domain)
        if match:
            year = match['year']
            event = match['event']
            return f"{event}{year}"

    if settings.DEBUG:
        return "tracon2020"
    else:
        raise ValueError(f"Could not deduce event from domain: {domain}")