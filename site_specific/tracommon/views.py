from content.models import SiteSettings

from .models import Artist


def front_page_controller(request, page, num_blog_posts=5):
    current_site_settings = request.site.site_settings
    blog_site_settings = SiteSettings.objects.get(site__domain='blog.tracon.fi')

    return dict(
        blog_posts=blog_site_settings.get_visible_blog_posts()[:num_blog_posts],
        news_posts=current_site_settings.get_visible_blog_posts()[:num_blog_posts],
        blog_index_url=blog_site_settings.get_protocol_relative_uri('content_blog_index_view'),
    )


def artists_alley_page_controller(request, page):
    return dict(artists=Artist.objects.filter(site=request.site))
