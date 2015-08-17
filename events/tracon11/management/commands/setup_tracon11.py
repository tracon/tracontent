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
    help = 'Setup example content'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=unicode)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print 'NOTE: Setting up Tracon 11 site at {domain}'.format(domain=self.domain)
        self.setup_site()
        self.setup_content()
        self.setup_ads()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain)

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                title='Tracon 11',
                base_template='tracon11_base.jade',
                page_template='tracon11_page.jade',
                blog_index_template='tracon11_blog_index.jade',
                blog_post_template='tracon11_blog_post.jade',
            )
        )

        # v3
        if self.site_settings.page_template == 'example_page.jade':
            self.site_settings.page_template = 'tracon11_page.jade'
        if self.site_settings.blog_index_template == 'example_blog_index.jade':
            self.site_settings.blog_index_template = 'tracon11_blog_index.jade'
        if self.site_settings.blog_post_template == 'example_blog_post.jade':
            self.site_settings.blog_post_template = 'tracon11_blog_post.jade'

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', u'Tracon 11 Tampere-talossa 3.–4. syyskuuta 2016', []),
            ('blog', u'Ajankohtaista', []), # pseudo page for menu, actually taken over by blog
            ('tapahtuma', u'Tapahtuma', [
                ('tyovoima', u'Vänkäriksi'),
                ('jarjestyssaannot', u'Järjestyssäännöt'),
                ('tapahtumapaikka', u'Tapahtumapaikka'),
            ]),
            ('ohjelma', u'Ohjelma', [
                ('ohjelmanjarjestajaksi', u'Ohjelmanjärjestäjäksi'),
            ]),
            ('liput', u'Liput', []),
            ('yhteys', u'Ota yhteyttä!', [
                ('conitea', u'Järjestäjät'),
                ('media', u'Tiedotusvälineille'),
                ('sponsorit', u'Yhteistyökumppaneille'),
            ])
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

            # v2
            if parent_page.order == 0:
                parent_page.order = ordering
                parent_page.save()

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

                # v2
                if child_page.order == 0:
                    child_page.order = child_ordering
                    child_page.save()

        front_page = Page.objects.get(site=self.site, slug='front-page')
        if not front_page.override_menu_text:
            front_page.override_menu_text = 'Etusivu'
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

    def setup_ads(self):
        for banner_title, banner_url, banner_path in [
            (u'Säätöyhteisö B2 ry', 'http://b2.fi', 'events/tracon11/static/tracon11/img/b2-saatoa2008-wh-200.png'),
        ]:
            try:
                Banner.objects.get(site=self.site, url=banner_url)
            except Banner.DoesNotExist:
                with open(banner_path) as banner_file:
                    Banner(
                        site=self.site,
                        title=banner_title,
                        url=banner_url,
                        image_file=File(banner_file),
                    ).save()
