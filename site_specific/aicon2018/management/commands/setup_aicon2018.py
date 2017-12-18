# encoding: utf-8

from __future__ import print_function, unicode_literals

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
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print('NOTE: Setting up Aicon site at {domain}'.format(domain=self.domain))
        self.setup_site()
        self.setup_content()
        self.setup_ads()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, name=u'Aicon')

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='aicon2018_base.jade',
                page_template='aicon2018_page.jade',
                blog_index_template='aicon2018_blog_index.jade',
                blog_post_template='aicon2018_blog_post.jade',
            )
        )

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', 'Tulossa 2018', []),
            ('blog', 'Ajankohtaista', []), # pseudo page for menu, actually taken over by blog
            ('tapahtuma', 'Tapahtuma', []),
            ('ohjelma', 'Ohjelma', []),
            ('yhteys', 'Yhteystiedot', [
                ('medialle', 'Medialle'),
                ('sponsoriksi', 'Sponsoriksi'),
            ]),
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

        front_page = Page.objects.get(site=self.site, slug='front-page')
        if front_page.title == 'Aicon':
            front_page.title = 'Tulossa 2018'
        if not front_page.override_menu_text:
            front_page.override_menu_text = 'Etusivu'
        if not front_page.override_page_template:
            front_page.override_page_template = 'aicon2018_front_page.jade'
        if not front_page.page_controller_code:
            front_page.page_controller_code = 'site_specific.aicon2018.views:front_page_controller'
        if 'Placeholder for front-page' in front_page.body or 'Lorem ipsum' in front_page.body:
            front_page.body = 'Aicon on aasialaiseen musiikkiin ja muotiin keskittyvä kaksipäiväinen tapahtuma, joka järjestään toisen kerran kesällä 2018. Aicon tarjoaa kävijöilleen monipuolista ohjelmaa ja tekemistä täysin omannäköisellään vivahteella, ja toivottaa kaikki aiheesta kiinnostuneet tervetulleiksi tapahtumaan!'
        front_page.save()

        organizers_page = Page.objects.get(site=self.site, slug='yhteys')
        organizers_page.override_page_template = 'aicon2018_organizers_page.jade'
        organizers_page.page_controller_code = 'site_specific.aicon2018.views:organizers_page_controller'
        organizers_page.save()

        programme_page = Page.objects.get(site=self.site, path='ohjelma')
        programme_page.page_controller_code = 'site_specific.aicon2018.views:programme_page_controller'
        programme_page.override_page_template = 'aicon2018_programme_page.jade'
        programme_page.save()

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
                'Japan-poppia, minun conissani!?!',
                'Aiconin kävijäkysely',
                'Seuraa Aiconia Twitterissä ja Facebookissa!',
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
            'aicon2018.css',
            'aicon2018_tracontent.css',
        ]:
            stylesheet_path = os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'static', 'aicon2018', 'css',
                stylesheet_name
            )

            with open(stylesheet_path) as input_file:
                StyleSheet.ingest(input_file)

    def setup_ads(self):
        for banner_title, banner_url, banner_path in [
            ('Bard & Jester', 'http://bardjester.com/', 'site_specific/aicon2018/static/aicon2018/img/BJDark.jpg'),
            ('Winkie Winkie', 'https://www.winkie-winkie.com/', 'site_specific/aicon2018/static/aicon2018/img/winkiemainos.jpg'),
        ]:
            try:
                Banner.objects.get(sites=self.site, url=banner_url)
            except Banner.DoesNotExist:
                with open(banner_path, 'rb') as banner_file:
                    banner = Banner(
                        title=banner_title,
                        url=banner_url,
                        image_file=File(banner_file),
                    )

                    banner.save()

                    banner.sites = [self.site,]
                    banner.save()
