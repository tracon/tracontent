# encoding: utf-8

from __future__ import print_function, unicode_literals

from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from content.models import Page, Redirect, SiteSettings, BlogPost, BlogCategory
from ads.models import Banner


class Command(BaseCommand):
    args = ''
    help = 'Setup conikuvat site'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print('NOTE: Setting up conikuvat site at {domain}'.format(domain=self.domain))
        self.setup_site()
        self.setup_content()
        self.setup_ads()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, defaults=dict(
            name='Conikuvat.fi',
        ))

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='conikuvat_base.jade',
                page_template='conikuvat_page.jade',
                blog_index_template='conikuvat_blog_index.jade',
                blog_post_template='conikuvat_blog_post.jade',
            )
        )

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', 'Etusivu', []),
            ('blog', 'Ajankohtaista', []), # pseudo page for menu, actually taken over by blog
        ]:
            ordering += 10

            parent_page, unused = Page.objects.get_or_create(
                site=self.site,
                parent=None,
                slug=page_slug,
                defaults=dict(
                    title=page_title,
                    body='Placeholder for {slug}'.format(slug=page_slug),
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
                        body='Placeholder for {slug}'.format(slug=child_slug),
                        public_from=t,
                        visible_from=t,
                        order=child_ordering,
                    )
                )

        front_page = Page.objects.get(site=self.site, path='front-page')
        if not front_page.override_page_template:
            front_page.override_page_template = 'conikuvat_front_page.jade'
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
            ('Säätöyhteisö B2 ry', 'http://b2.fi', 'site_specific/tracon11/static/tracon11/img/b2-saatoa2008-wh-200.png'),
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

