from collections import defaultdict

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from reversion.models import Version
from tabulate import tabulate

from content.models import Page


class Command(BaseCommand):
    args = ""
    help = "Get usernames of people who have edited pages"

    def handle(self, *args, **options):
        for site in Site.objects.all():
            pages = Page.objects.filter(site=site)
            editors: defaultdict[str, int] = defaultdict(int)

            for page in pages:
                for version in Version.objects.get_for_object(page):  # type: ignore
                    if version.revision.user and version.revision.user.is_authenticated:
                        editors[version.revision.user.username] += 1

            editors_sorted = sorted(editors.items(), key=lambda x: x[1], reverse=True)
            editors_sorted.append(("TOTAL", sum([x[1] for x in editors_sorted])))

            print(site.domain)
            print()
            print(tabulate(editors_sorted, headers=["editor", "# edits"]))
            print()
            print()
