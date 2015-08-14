# encoding: utf-8

from datetime import datetime, timedelta, date

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from content.models import Page, Redirect, SiteSettings, BlogPost


class Command(BaseCommand):
    args = ''
    help = 'Setup example content'

    def handle(self, *args, **options):
        t = now()

        site, unused = Site.objects.get_or_create(domain='tracontent.dev:8000')
        root_page, unused = Page.objects.get_or_create(
            site=site,
            parent=None,
            slug='front-page',
            defaults=dict(
                title='Welcome to your example site',
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

        for path, target in [
            ('admin', '/admin/'),
        ]:
            redirect, unused = Redirect.objects.get_or_create(
                site=site,
                path=path,
                defaults=dict(
                    target=target
                ),
            )