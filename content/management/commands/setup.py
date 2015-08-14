# encoding: utf-8

from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    args = ''
    help = 'Setup all the things'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', default=False)

    def handle(self, *args, **options):
        test = options['test']

        management_commands = [
            (('collectstatic',), dict(interactive=False)),
            (('migrate',), dict()),
        ]

        for pargs, opts in management_commands:
            call_command(*pargs, **opts)

        if test:
            user, created = User.objects.get_or_create(
                username='mahti',
                is_staff=True,
                is_superuser=True,
            )

            if created:
                user.set_password('mahti')
                user.save()
                print 'WARNING: Creating superuser "mahti" with password "mahti"'
