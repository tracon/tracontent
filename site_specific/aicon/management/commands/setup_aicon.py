# encoding: utf-8

from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from content.models import Page, Redirect, SiteSettings, BlogPost
from ads.models import Banner


class Command(BaseCommand):
    args = ''
    help = 'Setup Aicon site'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=unicode)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print 'NOTE: Setting up Aicon site at {domain}'.format(domain=self.domain)
        self.setup_site()
        self.setup_content()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, name=u'Aicon')

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='aicon_base.jade',
                page_template='aicon_page.jade',
                blog_index_template='aicon_blog_index.jade',
                blog_post_template='aicon_blog_post.jade',
            )
        )

        # v3
        if self.site_settings.page_template == 'example_page.jade':
            self.site_settings.page_template = 'aicon_page.jade'
        if self.site_settings.blog_index_template == 'example_blog_index.jade':
            self.site_settings.blog_index_template = 'aicon_blog_index.jade'
        if self.site_settings.blog_post_template == 'example_blog_post.jade':
            self.site_settings.blog_post_template = 'aicon_blog_post.jade'

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', u'Aicon', []),
            ('blog', u'Ajankohtaista', []), # pseudo page for menu, actually taken over by blog
            ('tapahtuma', u'Tapahtuma', []),
            ('ohjelma', u'Ohjelma', []),
            ('yhteys', u'Yhteystiedot', [])
        ]:
            ordering += 10

            parent_page, unused = Page.objects.get_or_create(
                site=self.site,
                parent=None,
                slug=page_slug,
                defaults=dict(
                    title=page_title,
                    body=u'Placeholder for {slug}'.format(slug=page_slug),
                    public_from=t,
                    visible_from=t,
                    order=ordering,
                )
            )

            child_ordering = 0
            for child_slug, child_title in child_pages:
                child_ordering += 10

                child_page, unused = Page.objects.get_or_create(
                    site=self.site,
                    parent=parent_page,
                    slug=child_slug,
                    defaults=dict(
                        title=child_title,
                        body=u'Placeholder for {slug}'.format(slug=child_slug),
                        public_from=t,
                        visible_from=t,
                        order=child_ordering,
                    )
                )

        front_page = Page.objects.get(slug='front-page')
        if not front_page.override_menu_text:
            front_page.override_menu_text = u'Etusivu'

        for path, target in [
            ('admin', '/admin/'),
        ]:
            redirect, unused = Redirect.objects.get_or_create(
                site=self.site,
                path=path,
                defaults=dict(
                    target=target
                ),
            )
