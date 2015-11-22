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
        print 'NOTE: Setting up Tracon Hitpoint 2015 site at {domain}'.format(domain=self.domain)
        self.setup_site()
        self.setup_content()
        self.setup_ads()
        self.setup_blog()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, name=u'Tracon Hitpoint 2015')

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='hitpoint2015_base.jade',
                page_template='hitpoint2015_page.jade',
                blog_index_template='hitpoint2015_blog_index.jade',
                blog_post_template='hitpoint2015_blog_post.jade',
                context_processor_code='site_specific.hitpoint2015.context_processors:hitpoint2015_context',
            )
        )

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', u'Dummy etusivu', []),

            # Outside fi subsite for technical reasons
            ('blog', u'Ajankohtaista', []),

            ('fi', u'Kaksi päivää pelaamista Tampereen keskustassa!', [
                ('tapahtuma', u'Tapahtuma'),
                ('liput', u'Lipunmyynti'),
                ('goh', u'Kunniavieraat'),
                ('ohjelma', u'Ohjelma'),
            ]),

            ('en', u'Two days of table-top games in Downtown Tampere!', [
                ('tickets', u'Tickets'),
                ('goh', u'Guests of Honour'),
            ]),
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

        fi_front_page = Page.objects.get(site=self.site, parent=None, slug='fi')
        if not fi_front_page.override_page_template:
            fi_front_page.override_page_template = 'hitpoint2015_front_page.jade'
        if not fi_front_page.page_controller_code:
            fi_front_page.page_controller_code = 'site_specific.tracommon.views:front_page_controller'
        fi_front_page.save()

        programme_page = Page.objects.get(site=self.site, path='fi/ohjelma')
        if not programme_page.page_controller_code:
            programme_page.page_controller_code = 'site_specific.hitpoint2015.views:programme_page_controller'
        if not programme_page.override_page_template:
            programme_page.override_page_template = 'hitpoint2015_programme_page.jade'
        programme_page.save()

        for path, target in [
            ('admin', '/admin/'),
            ('front-page', '/fi'),
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
            (u'Säätöyhteisö B2 ry', 'http://b2.fi', 'site_specific/tracon11/static/tracon11/img/b2-saatoa2008-wh-200.png'),
        ]:
            try:
                banner = Banner.objects.get(url=banner_url)
                banner.sites.add(self.site)
            except Banner.DoesNotExist:
                with open(banner_path) as banner_file:
                    banner = Banner(
                        title=banner_title,
                        url=banner_url,
                        image_file=File(banner_file),
                    )

                    banner.save()

                    banner.sites = [self.site,]
                    banner.save()

    def setup_blog(self):
        """
        Set up a stub of the blog.tracon.fi site required by the front page blog box.
        """
        blog_site, unused = Site.objects.get_or_create(domain='blog.tracon.fi', defaults=dict(
            name='Traconin blogi'
        ))
        blog_site_settings, unused = SiteSettings.objects.get_or_create(site=blog_site, defaults=dict(
            base_template='tracon11_base.jade',
            page_template='tracon11_page.jade',
            blog_index_template='tracon11_blog_index.jade',
            blog_post_template='tracon11_blog_post.jade',
        ))
