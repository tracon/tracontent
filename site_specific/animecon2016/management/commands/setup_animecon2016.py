import os

from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ads.models import Banner
from content.models import Page, Redirect, SiteSettings, BlogPost
from resources.models import StyleSheet


class Command(BaseCommand):
    args = ''
    help = 'Setup Animecon 2016 site'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print(f'NOTE: Setting up Animecon 2016 site at {self.domain}')
        self.setup_site()
        self.setup_content()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, name='Animecon 2016')

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='animecon2016_base.jade',
                page_template='animecon2016_page.jade',
                blog_index_template='animecon2016_blog_index.jade',
                blog_post_template='animecon2016_blog_post.jade',
                context_processor_code='site_specific.animecon2016.context_processors:animecon2016_context',
            )
        )

        if not self.site_settings.context_processor_code:
            self.site_settings.context_processor_code = 'site_specific.animecon2016.context_processors:animecon2016_context'
            self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', 'Dummy etusivu', []),

            # Outside fi subsite for technical reasons
            ('blog', 'Ajankohtaista', []),

            ('fi', 'Animecon 2016', [
                ('front-page', 'Etusivu'),
                ('blog', 'Ajankohtaista'), # pseudo page for menu, actually taken over by blog
                ('tapahtuma', 'Tapahtuma'),
                ('ohjelma', 'Ohjelma'),
                ('liput', 'Liput'),
                ('yhteys', 'Ota yhteyttä!'),
            ]),

            ('en', 'Animecon 2016 in English', [
                ('front-page', 'Front page'),
                ('event', 'Event'),
                ('program', 'Program'),
                ('tickets', 'Tickets'),
                ('contact', 'Contact us!'),
            ]),
        ]:
            ordering += 10

            parent_page, unused = Page.objects.get_or_create(
                site=self.site,
                parent=None,
                slug=page_slug,
                defaults=dict(
                    title=page_title,
                    body=f'Placeholder for {page_slug}',
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
                        body=f'Placeholder for {child_slug}',
                        public_from=t,
                        visible_from=t,
                        order=child_ordering,
                    )
                )

        programme_page = Page.objects.get(site=self.site, path='fi/ohjelma')
        programme_page.page_controller_code = 'site_specific.animecon2016.views:programme_page_controller'
        programme_page.override_page_template = 'animecon2016_programme_page.jade'
        programme_page.save()

        for path, target in [
            ('admin', '/admin/'),
            ('fi', '/fi/front-page'),
            ('en', '/en/front-page'),
            ('front-page', '/fi/front-page'),
        ]:
            redirect, unused = Redirect.objects.get_or_create(
                site=self.site,
                path=path,
                defaults=dict(
                    target=target
                ),
            )

        for stylesheet_name in [
            'layout.css',
            'style.css',
            'usermenu.css',
        ]:
            stylesheet_path = os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'static', 'animecon2016', 'css',
                stylesheet_name
            )

            with open(stylesheet_path) as input_file:
                StyleSheet.ingest(input_file)
