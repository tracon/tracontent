from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_safe

from ipware.ip import get_ip

from .models import Page, BlogPost, Redirect
from .forms import BlogCommentForm
from .utils import initialize_form


@require_safe
def content_page_view(request, path):
    site_settings = request.site.site_settings

    # Look for redirect at the current path
    try:
        current_url_redirect = Redirect.objects.get(site=request.site, path=path)
    except Redirect.DoesNotExist:
        pass
    else:
        return redirect(current_url_redirect.target)

    criteria = dict(site=request.site, path=path)

    if not request.user.is_staff:
        # Only show published pages
        criteria.update(public_from__lte=now())

    # Look for page at the current path
    page = get_object_or_404(Page, **criteria)

    return page.render(request)


@require_safe
def content_blog_index_view(request):
    site_settings = request.site.site_settings

    # Look for redirect at the current path
    try:
        current_url_redirect = Redirect.objects.get(site=request.site, path=request.path[1:])
    except Redirect.DoesNotExist:
        pass
    else:
        return redirect(current_url_redirect.target)

    criteria = dict(site=request.site, path='blog')

    if not request.user.is_staff:
        # Only show published pages
        criteria.update(public_from__lte=now())

    page = get_object_or_404(Page, **criteria)

    vars = dict(
        page=page,
        blog_posts=site_settings.get_visible_blog_posts(),
    )

    return render(request, site_settings.blog_index_template, vars)


@require_http_methods(['GET', 'HEAD', 'POST'])
def content_blog_post_view(request, year, month, day, slug):
    site_settings = request.site.site_settings

    # Look for redirect at the current path
    try:
        current_url_redirect = Redirect.objects.get(site=request.site, path=request.path[1:])
    except Redirect.DoesNotExist:
        pass
    else:
        return redirect(current_url_redirect.target)

    try:
        post_date = date(int(year), int(month), int(day))
    except ValueError:
        raise Http404(u'Invalid date')

    criteria = dict(site=request.site, date=post_date, slug=slug)

    if not request.user.is_staff:
        # Only show published blog posts
        criteria.update(public_from__lte=now())

    blog_post = get_object_or_404(BlogPost, **criteria)

    blog_comment_form = initialize_form(BlogCommentForm, request)

    if request.method == 'POST' and blog_comment_form.is_valid():
        blog_comment = blog_comment_form.save(commit=False)
        blog_comment.blog_post = blog_post
        blog_comment.author_ip_address = get_ip(request)
        blog_comment.save()

        blog_comment.send_mail_to_moderators(request)

        return redirect(blog_post.get_absolute_url())

    return blog_post.render(request,
        blog_post=blog_post,
        blog_comment_form=blog_comment_form,
        blog_comments=list(blog_post.get_comments()),
    )

