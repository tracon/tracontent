from collections import namedtuple

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse

from .models import BlogPost


class BlogFeedRSS(Feed):
    def get_object(self, request, *args, **kwargs):
        return request

    def title(self, request):
        return request.site.site_settings.title

    def link(self, request):
        return request.build_absolute_uri(reverse('content_blog_index_view'))

    def description(self, request):
        return request.site.site_settings.description

    def items(self, request):
        return request.site.site_settings.get_visible_blog_posts()

    def item_title(self, blog_post):
        return blog_post.title

    def item_description(self, blog_post):
        return blog_post.excerpt

    def item_author_name(self, blog_post):
        return blog_post.author.get_full_name()

    def item_updateddate(self, blog_post):
        return blog_post.public_from


class BlogFeedAtom(BlogFeedRSS):
    feed_type = Atom1Feed
    subtitle = BlogFeedRSS.description
