from content.models import SiteSettings

from .models import Organizer

from ..tracommon.utils import kompassi_get_programme


def front_page_controller(request, page, num_blog_posts=5):
    current_site_settings = request.site.site_settings

    return dict(
        news_posts=current_site_settings.get_visible_blog_posts()[:num_blog_posts],
    )


def organizers_page_controller(request, page, num_organizers_per_row=5):
    organizers = Organizer.objects.all()

    return dict(
        organizers=organizers,
    )


def programme_page_controller(request, page, event_slug='aicon2016'):
    programme = kompassi_get_programme(event_slug)

    return dict(
        programme=programme,
    )
