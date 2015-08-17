from django.conf.urls import patterns, include, url

from .views import (
    content_page_view,
    content_blog_post_view,
    content_blog_index_view,
)
from .feeds import BlogFeedRSS, BlogFeedAtom


urlpatterns = patterns('',
    url(
        r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[a-z0-9-]+)/?$',
        content_blog_post_view,
        name='content_blog_post_view',
    ),

    url(
        r'^blog/rss/?$',
        BlogFeedRSS(),
        name='content_blog_feed_rss_view',
    ),

    url(
        r'^blog/atom/?$',
        BlogFeedAtom(),
        name='content_blog_feed_atom_view',
    ),

    url(
        r'^blog/?$',
        content_blog_index_view,
        name='content_blog_index_view',
    ),

    url(
        r'^(?P<path>[a-z0-9-]+(/[a-z0-9-]+)*)/?$',
        content_page_view,
        name='content_page_view',
    ),

    url(
        r'^$',
        content_page_view,
        dict(path='front-page'),
        name='content_front_page_view',
    ),
)
