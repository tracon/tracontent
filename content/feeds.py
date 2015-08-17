from collections import namedtuple

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site

from .models import BlogPost


FeedContext = namedtuple('FeedContext', 'site request')


class BlogFeedRSS(Feed):
    def get_object(self, request, *args, **kwargs):
        return FeedContext(
            site=get_current_site(request),
            request=request,
        )

    def title(self, feed_context):
        return feed_context.site.site_settings.title

    def link(self, feed_context):
        return feed_context.request.build_absolute_uri(reverse('content_blog_index_view'))

    def description(self, feed_context):
        return feed_context.site.site_settings.description

    def items(self, feed_context):
        return feed_context.site.site_settings.get_visible_blog_posts()

    def item_title(self, blog_post):
        return blog_post.title

    def item_description(self, blog_post):
        return blog_post.excerpt

    def item_author_name(self, blog_post):
        return blog_post.author.get_full_name()

    def item_updateddate(self, blog_post):
        return blog_post.updated_at


class BlogFeedAtom(BlogFeedRSS):
    feed_type = Atom1Feed
    subtitle = BlogFeedRSS.description
