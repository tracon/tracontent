# encoding: utf-8

from datetime import datetime, timedelta, date

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class Command(BaseCommand):
    args = ''
    help = 'Setup example content'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=unicode)

    def handle(self, *args, **options):
        self.setup_content(domain=options['domain'])

    def setup_content(self, domain):
        from django.contrib.sites.models import Site
        from django.contrib.auth.models import User
        from content.models import Page, Redirect, SiteSettings, BlogPost

        t = now()

        print 'NOTE: Setting up Tracon 11 site at {domain}'.format(domain=domain)

        site, unused = Site.objects.get_or_create(domain=domain)

        site_settings, unused = SiteSettings.objects.get_or_create(
            site=site,
            defaults=dict(
                title='Tracon 11',
                base_template='tracon11_base.jade',
                page_template='tracon11_base.jade',
            )
        )

        # v3
        if site_settings.page_template == 'example_page.jade':
            site_settings.page_template = 'tracon11_page.jade'
            site_settings.save()

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
                site=site,
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
                    site=site,
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

        front_page = Page.objects.get(site=site, slug='front-page')
        if not front_page.override_menu_text:
            front_page.override_menu_text = 'Etusivu'
            front_page.save()

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
