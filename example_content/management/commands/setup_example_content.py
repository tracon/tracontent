# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class Command(BaseCommand):
    args = ''
    help = 'Setup example content'

    def handle(self, *args, **options):
        self.run_other_commands()
        self.setup_content()

    def run_other_commands(self):
        management_commands = [
            (('collectstatic',), dict(interactive=False)),
            (('migrate',), dict()),
        ]

        for pargs, opts in management_commands:
            call_command(*pargs, **opts)


    def setup_content(self):
        from django.contrib.sites.models import Site
        from django.contrib.auth.models import User
        from content.models import Page, Redirect

        t = now()

        site, unused = Site.objects.get_or_create(domain='tracontent.dev:8000')
        root_page, unused = Page.objects.get_or_create(
            site=site,
            parent=None,
            slug='',
            defaults=dict(
                title='Root page',
                body='',
                public_from=t,
                visible_from=t,
            )
        )

        redirect, unused = Redirect.objects.get_or_create(
            site=site,
            path='admin',
            defaults=dict(target='/admin/'),
        )

        user, created = User.objects.get_or_create(
            username='mahti',
            is_staff=True,
            is_superuser=True,
        )

        if created:
            user.set_password('mahti')
            user.save()
