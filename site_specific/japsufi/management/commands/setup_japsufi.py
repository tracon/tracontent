from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from content.models import Page, Redirect, SiteSettings, BlogPost
from content.utils import lorem
from ads.models import Banner


class Command(BaseCommand):
    args = ''
    help = 'Setup example content'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        Setup(domain=options['domain']).setup()


class Setup(object):
    def __init__(self, domain):
        self.domain = domain

    def setup(self):
        print(f'NOTE: Setting up japsu.fi site at {self.domain}')
        self.setup_site()
        self.setup_content()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, name='Japsu.fi')

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='japsufi_base.jade',
                page_template='japsufi_page.jade',
                blog_index_template='japsufi_blog_index.jade',
                blog_post_template='japsufi_blog_post.jade',
            )
        )

        ordering = 0
        for page_data in [
            ('front-page', 'Japsu.fi', 'Etusivu', []),
            ('blog', 'Blogi', []), # pseudo page for menu, actually taken over by blog
            ('kuvat', 'Valokuvia', []),
            ('projektit', 'Projektit', []),
            ('yhteys', 'Ota yhteyttä!', [])
        ]:
            if len(page_data) == 3:
                page_slug, page_title, child_pages = page_data
                override_menu_text = ''
            elif len(page_data) == 4:
                page_slug, page_title, override_menu_text, child_pages = page_data
            else:
                raise NotImplementedError(len(page_data))

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
                    override_menu_text=override_menu_text,
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
