from content.models import SiteSettings
from content.utils import groups_of_n

from .models import Organizer


def front_page_controller(request, page, num_blog_posts=5):
    current_site_settings = request.site.site_settings

    return dict(
        news_posts=current_site_settings.get_visible_blog_posts()[:num_blog_posts],
    )


def organizers_page_controller(request, page, num_organizers_per_row=5):
    organizers = Organizer.objects.all()
    organizer_rows = groups_of_n(organizers, num_organizers_per_row)

    return dict(
        organizer_rows=organizer_rows,
    )
