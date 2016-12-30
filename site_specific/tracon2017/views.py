from content.models import SiteSettings

from site_specific.tracommon.utils import kompassi_get_programme


def miitit_page_controller(request, page, event_slug='tracon2017'):
    programme = kompassi_get_programme(event_slug, special=True, category='miitti')

    return dict(
        programme=programme,
    )
