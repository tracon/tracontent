
from .views import (
    content_cached_page_view,
    content_page_view,
    content_blog_post_view,
    content_blog_index_view,
)
from .feeds import BlogFeedRSS, BlogFeedAtom
from django.urls import path, re_path


urlpatterns = [
    re_path(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[a-z0-9-]+)/?$',
        content_blog_post_view,
        name='content_blog_post_view',
    ),

    re_path(r'^blog/rss/?$',
        BlogFeedRSS(),
        name='content_blog_feed_rss_view',
    ),

    re_path(r'^blog/atom/?$',
        BlogFeedAtom(),
        name='content_blog_feed_atom_view',
    ),

    re_path(r'^blog/?$',
        content_blog_index_view,
        name='content_blog_index_view',
    ),

    re_path(r'^blog/category/(?P<category_slug>[a-z0-9-]+)/?$',
        content_blog_index_view,
        name='content_blog_category_index_view',
    ),

    # CACHED PAGES
    # url(
    #     r'^(?P<path>liput)/?$',
    #     content_cached_page_view,
    #     name='content_cached_page_view_liput',
    # ),
    # url(
    #     r'^$',
    #     content_cached_page_view,
    #     dict(path='front-page'),
    #     name='content_front_page_view',
    # ),

    re_path(r'^(?P<path>[a-z0-9-]+(/[a-z0-9-]+)*)/?$',
        content_page_view,
        name='content_page_view',
    ),

    # NON-CACHED FRONT PAGE
    path('', content_page_view,
        dict(path='front-page'),
        name='content_front_page_view',
    ),
]
