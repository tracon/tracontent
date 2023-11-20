from django.contrib.sites.models import Site
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from reversion.models import Version

from content.models import Page, Redirect, SiteSettings, BlogCategory
from ads.models import Banner


class Command(BaseCommand):
    args = ""
    help = "Get usernames of people who have edited pages"

    def handle(self, *args, **options):
        for site in Site.objects.all():
            pages = Page.objects.filter(site=site)
            editors = {
                version.revision.user.username
                for page in pages
                for version in Version.objects.get_for_object(page)
                if version.revision.user
            }

            print(
                "{site} ({num_editors}): {editors}".format(
                    site=site,
                    num_editors=len(editors),
                    editors=", ".join(editors),
                )
            )
