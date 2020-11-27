import argparse

from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import Template


class Command(BaseCommand):
    args = ''
    help = 'Load templates into the database'

    def add_arguments(self, parser):
        parser.add_argument('--force', '-f',
            action='store_true',
            default=False,
            help='load template even though the one in the database were newer',
        )
        parser.add_argument('templates',
            metavar='FILE',
            type=argparse.FileType('r'),
            nargs='+',
            help='templates to load',
        )

    def handle(self, *args, **opts):
        for open_file in opts['templates']:
            Template.ingest(open_file, force=opts['force'])
            open_file.close()