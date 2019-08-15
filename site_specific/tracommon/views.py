from content.models import SiteSettings

from .models import Artist, DAY_CHOICES


def front_page_controller(request, page, num_blog_posts=5):
    current_site_settings = request.site.site_settings
    blog_site_settings = SiteSettings.objects.get(site__domain='blog.tracon.fi')

    return dict(
        blog_posts=blog_site_settings.get_visible_blog_posts()[:num_blog_posts],
        news_posts=current_site_settings.get_visible_blog_posts()[:num_blog_posts],
        blog_index_url=blog_site_settings.get_protocol_relative_uri('content_blog_index_view'),
    )


def artists_alley_page_controller(request, page):
    criteria = dict(site=request.site)

    day = request.GET.get('day')
    if day:
        criteria.update(day=day)

    return dict(
        artists=Artist.objects.filter(**criteria),
        artist_filters=[(key, text, key == day) for (key, text) in DAY_CHOICES],
    )
