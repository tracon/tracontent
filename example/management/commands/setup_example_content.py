# encoding: utf-8

from datetime import datetime, timedelta, date

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
        from content.models import Page, Redirect, SiteSettings, BlogPost

        t = now()

        site, unused = Site.objects.get_or_create(domain='tracontent.dev:8000')
        root_page, unused = Page.objects.get_or_create(
            site=site,
            parent=None,
            slug='',
            defaults=dict(
                title='',
                body='<p>This is the front page.</p>',
                public_from=t,
                visible_from=t,
            )
        )

        blog_post, unused = BlogPost.objects.get_or_create(
            site=site,
            slug='example-blog-post',
            defaults=dict(
                date=date(2015, 8, 13),
                title='Example blog post',
                body='<p>This is an example blog post.</p>',
                public_from=t,
                visible_from=t,
            )
        )

        site_settings, unused = SiteSettings.objects.get_or_create(
            site=site,
            defaults=dict(
                title='Example site',
                base_template='example_base.jade',
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
