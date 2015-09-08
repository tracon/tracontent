from content.models import SiteSettings


def front_page_controller(request, page):
    current_site_settings = request.site.site_settings
    blog_site_settings = SiteSettings.objects.get(site__domain='blog.tracon.fi')

    return dict(
        blog_posts=blog_site_settings.get_visible_blog_posts(),
        news_posts=current_site_settings.get_visible_blog_posts(),
      )
