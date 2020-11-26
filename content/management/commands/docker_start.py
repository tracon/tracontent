from os import environ

import logging
import time

from django.conf import settings
from django.db import ProgrammingError
from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger('kompassi')


class Command(BaseCommand):
    args = ''
    help = 'Docker development environment entry point'

    def handle(self, *args, **options):
        from content.models import SiteSettings

        test = settings.DEBUG
        site = environ.get('TRACONTENT_SITE', 'tracon2017')
        hostname = environ.get('TRACONTENT_HOSTNAME', 'localhost')

        if not test:
            raise ValueError('Should run with DEBUG=true')

        try:
            SiteSettings.objects.first()
        except ProgrammingError:
            call_command('setup')
            call_command(f'setup_{site}', f'{hostname}:8001')

        call_command('runserver', '0.0.0.0:8001')
