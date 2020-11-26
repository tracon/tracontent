from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from content.models import Page, Redirect, SiteSettings, BlogCategory
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
        print(f'NOTE: Setting up Tracon (2019) site at {self.domain}')
        self.setup_site()
        self.setup_content()
        self.setup_ads()
        self.setup_blog()

    def setup_site(self):
        self.site, unused = Site.objects.get_or_create(domain=self.domain, defaults=dict(
            name='Tracon (2019)',
        ))

    def setup_content(self):
        t = now()

        self.site_settings, unused = SiteSettings.objects.get_or_create(
            site=self.site,
            defaults=dict(
                base_template='tracon2019_base.jade',
                page_template='tracon2019_page.jade',
                blog_index_template='tracon2019_blog_index.jade',
                blog_post_template='tracon2019_blog_post.jade',
            )
        )

        self.site_settings.save()

        ordering = 0
        for page_slug, page_title, child_pages in [
            ('front-page', 'Tracon Tampere-talossa 7.–9.9.2019', []),
            ('blog', 'Ajankohtaista', []),  # pseudo page for menu, actually taken over by blog
            ('tapahtuma', 'Tapahtuma', [
                ('tyovoima', 'Vänkäriksi'),
                ('jarjestyssaannot', 'Järjestyssäännöt'),
                ('tapahtumapaikka', 'Tapahtumapaikka'),
                ('taidekuja', 'Taidekuja'),
            ]),
            ('ohjelma', 'Ohjelma', [
                ('ohjelmanjarjestajaksi', 'Ohjelmanjärjestäjäksi'),
            ]),
            # ('liput', 'Liput', []),
            ('yhteys', 'Ota yhteyttä!', [
                ('conitea', 'Järjestäjät'),
                ('media', 'Tiedotusvälineille'),
                ('sponsorit', 'Yhteistyökumppaneille'),
            ])
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

        front_page = Page.objects.get(site=self.site, slug='front-page')
        if not front_page.override_menu_text:
            front_page.override_menu_text = 'Etusivu'
        if not front_page.override_page_template:
            front_page.override_page_template = 'tracon2019_front_page.jade'
        if not front_page.page_controller_code or front_page.page_controller_code == 'events.tracommon.views:front_page_controller':
            front_page.page_controller_code = 'site_specific.tracommon.views:front_page_controller'
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

        programme_page = Page.objects.get(site=self.site, path='ohjelma')
        programme_miitit_page, created = Page.objects.get_or_create(
            site=self.site,
            parent=programme_page,
            slug='miitit',
            defaults=dict(
                title='Miitit',
                body='Placeholder',
                public_from=t,
                visible_from=t,
                page_controller_code='site_specific.tracon2019.views:miitit_page_controller',
                override_page_template='tracon2019_programme_page.jade',
                order=0,
            )
        )

        for path, template, controller in [
            ('yhteys/conitea', 'tracon2019_organizers_page.jade', 'site_specific.tracon2019.views:organizers_page_controller'),
            ('tapahtuma/taidekuja', 'tracon2019_artists_alley_page.jade', 'site_specific.tracommon.views:artists_alley_page_controller')
        ]:
            page = Page.objects.get(site=self.site, path=path)
            if not page.override_page_template:
                page.override_page_template = template
            if not page.page_controller_code:
                page.page_controller_code = controller
            page.save()

    def setup_ads(self):
        for banner_title, banner_url, banner_path in [
            ('Säätöyhteisö B2 ry', 'http://b2.fi', 'site_specific/tracon2019/static/tracon2019/img/b2-2016-200x-tr.png'),
            ('Conikuvat.fi', 'https://conikuvat.fi', 'site_specific/conikuvat/static/conikuvat/img/conikuvat-cu.svg'),
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

                    banner.sites.set([self.site,])
                    banner.save()

    def setup_blog(self):
        """
        Set up a stub of the blog.tracon.fi site required by the front page blog box.
        """
        blog_site, unused = Site.objects.get_or_create(domain='blog.tracon.fi', defaults=dict(
            name='Traconin blogi'
        ))
        blog_site_settings, unused = SiteSettings.objects.get_or_create(site=blog_site, defaults=dict(
            base_template='tracon2019_base.jade',
            page_template='tracon2019_page.jade',
            blog_index_template='tracon2019_blog_index.jade',
            blog_post_template='tracon2019_blog_post.jade',
        ))
