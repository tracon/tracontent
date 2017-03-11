from content.models import SiteSettings

from site_specific.tracommon.utils import kompassi_get_programme, kompassi_get_teams


def miitit_page_controller(request, page, event_slug='tracon2017'):
    programme = kompassi_get_programme(event_slug, special=True, category='miitti')

    return dict(
        programme=programme,
    )


def organizers_page_controller(request, page, event_slug='tracon2017'):
    teams = kompassi_get_teams(event_slug)

    return dict(
        teams=teams,
    )