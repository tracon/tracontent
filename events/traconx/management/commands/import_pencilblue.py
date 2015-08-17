# encoding: utf-8

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from pymongo import MongoClient

from content.models import Page
from content.utils import slugify


class Command(BaseCommand):
    args = ''
    help = 'Import a PencilBlue site'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=unicode)
        parser.add_argument('--mongo-username', type=unicode)
        parser.add_argument('--mongo-password', type=unicode)
        parser.add_argument('--mongo-database', type=unicode, default='tracon2015')
        parser.add_argument('--mongo-host', type=unicode, default='localhost')
        parser.add_argument('--mongo-port', type=int, default=27017)

    def handle(self, *args, **options):
        mongo_client = MongoClient(host=options['mongo_host'], port=options['mongo_port'])
        db = mongo_client[options['mongo_database']]

        if options.get('mongo_username'):
            db.authenticate(options['mongo_username'], options.get('mongo_password'))

        tc_site = Site.objects.get(domain=options['domain'])

        tc_root_page = Page.objects.get_or_create(
            site=tc_site,
            slug='imported',
            defaults=dict(
                title=u'PencilBluesta tuodut sivut',
                body=u'<p>Tämän sivun alasivut on tuotu automaattisesti PencilBluesta.</p>'
            )
        )

        for pb_page in db.page.find():
            Page.objects.get_or_create(
                site=tc_site,
                parent=tc_root_page,
                slug=slugify(pb_page['headline']),
                defaults=dict(
                    title=pb_page['headline'],
                    body=pb_page['page_layout'],
                )
            )
