from content.models import SiteSettings

from site_specific.tracommon.utils import kompassi_get_programme


def programme_page_controller(request, page, event_slug='hitpoint2017'):
    programme = kompassi_get_programme(event_slug)

    return dict(
        programme=programme,
    )
