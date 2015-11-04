# encoding: utf-8

import os.path
from datetime import datetime, timedelta, date

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ads.models import Banner
from content.models import Page, Redirect, SiteSettings, BlogPost
from content.utils import slugify, lorem
from resources.models import StyleSheet


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

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', u'Verkatehdas, Hämeenlinna, 8.–9.10.2016', []),
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
                    body=lorem(),
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
                        body=lorem(),
                        public_from=t,
                        visible_from=t,
                        order=child_ordering,
                    )
                )

        front_page = Page.objects.get(slug='front-page')
        if front_page.title == u'Aicon':
            front_page.title = u'Verkatehdas, Hämeenlinna, 8.–9.10.2016'
        if not front_page.override_menu_text:
            front_page.override_menu_text = u'Etusivu'
        if not front_page.override_page_template:
            front_page.override_page_template = 'aicon_front_page.jade'
        if not front_page.page_controller_code:
            front_page.page_controller_code = 'site_specific.aicon.views:front_page_controller'
        if 'Placeholder for front-page' in front_page.body or 'Lorem ipsum' in front_page.body:
            front_page.body = u'Aicon on aasialaiseen musiikkiin ja muotiin keskittyvä kaksipäiväinen tapahtuma, joka järjestään ensimmäistä kertaa syksyllä 2016. Aicon tarjoaa kävijöilleen monipuolista ohjelmaa ja tekemistä täysin omannäköisellään vivahteella, ja toivottaa kaikki aiheesta kiinnostuneet tervetulleiksi tapahtumaan!'
        front_page.save()

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

        if settings.DEBUG:
            d = date.today()

            for blog_title in [
                u'Japan-poppia, minun conissani!?!',
                u'Aiconin kävijäkysely',
                u'Seuraa Aiconia Twitterissä ja Facebookissa!',
            ]:
                blog_post, unused = BlogPost.objects.get_or_create(
                    site=self.site,
                    slug=slugify(blog_title),
                    defaults=dict(
                        date=d,
                        override_excerpt='blaa blaa blaa',
                        title=blog_title,
                        body='Dummy blog post',
                        public_from=t,
                        visible_from=t,
                    )
                )

        for stylesheet_name in [
            'aicon.css',
            'aicon_tracontent.css',
        ]:
            stylesheet_path = os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'static', 'aicon', 'css',
                stylesheet_name
            )

            with open(stylesheet_path) as input_file:
                StyleSheet.ingest(input_file)
