from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_safe

from ipware.ip import get_ip

from .models import Page, BlogPost, Redirect, RenderPageMixin, BlogCategory
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


class BlogIndexPseudoPage(RenderPageMixin):
    """
    Renders a default blog index into the site base template.
    """
    def __init__(self, site, title):
        self.site = site
        self.title = title
        self.body = u''
        self.template = site.site_settings.page_template


@require_safe
def content_blog_index_view(request, category_slug=None):
    site_settings = request.site.site_settings

    # Look for redirect at the current path
    try:
        current_url_redirect = Redirect.objects.get(site=request.site, path=request.path[1:])
    except Redirect.DoesNotExist:
        pass
    else:
        return redirect(current_url_redirect.target)

    page_criteria = dict(site=request.site)
    post_criteria = dict()

    if category_slug is not None:
        category = get_object_or_404(BlogCategory, site=request.site, slug=category_slug)
        page_criteria.update(path=category.path)
        post_criteria.update(categories=category)
    else:
        category = None
        page_criteria.update(path='blog')

    if not request.user.is_staff:
        # Only show published pages
        page_criteria.update(public_from__lte=now())

    try:
        page = Page.objects.get(**page_criteria)
    except Page.DoesNotExist:
        title = category.title if category else u'Blog'
        page = BlogIndexPseudoPage(request.site, title)

    vars = dict(
        page=page,
        blog_posts=site_settings.get_visible_blog_posts(**post_criteria),
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

    base_criteria = dict(site=request.site, slug=slug)

    if not request.user.is_staff:
        # Only show published blog posts
        base_criteria.update(public_from__lte=now())

    try:
        blog_post = BlogPost.objects.get(date=post_date, **base_criteria)
    except BlogPost.DoesNotExist:
        # The date may have been changed. If the slug is still unique, redirect to the new path.
        try:
            blog_post = get_object_or_404(BlogPost, **base_criteria)
        except BlogPost.MultipleObjectsReturned:
            raise Http404(u'Duplicate slug and wrong date')

        return redirect(blog_post.get_absolute_url())

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

