from datetime import date

from django.http import Http404, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now

from .models import Page, BlogPost, Redirect


def content_page_view(request, path):
    site = get_current_site(request)
    site_settings = site.site_settings

    # Look for redirect at the current path
    try:
        current_url_redirect = Redirect.objects.get(site=site, path=path)
    except Redirect.DoesNotExist:
        pass
    else:
        return redirect(current_url_redirect.target)

    criteria = dict(path=path)

    if not request.user.is_staff:
        # Only show published pages
        criteria.update(public_from__lte=now())

    # Look for page at the current path
    page = get_object_or_404(Page, **criteria)

    return page.render(request)


def content_blog_index_view(request):
    site = get_current_site(request)
    site_settings = site.site_settings

    blog_posts = site.blog_post_set.all()

    vars = dict(
        blog_posts=blog_posts,
    )

    return render(request, site_settings.blog_index_template, vars)


def content_blog_post_view(request, year, month, day, slug):
    site = get_current_site(request)
    site_settings = site.site_settings

    try:
        post_date = date(int(year), int(month), int(day))
    except ValueError:
        raise Http404(u'Invalid date')

    blog_post = get_object_or_404(BlogPost, site=site, date=post_date, slug=slug)
    return blog_post.render(request)
