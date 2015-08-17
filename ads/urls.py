from django.conf.urls import patterns, include, url

from .views import ads_banner_redirect_view


urlpatterns = patterns('',
    url(
        r'^banners/(?P<banner_id>\d+)/redirect/?$',
        ads_banner_redirect_view,
        name='ads_banner_redirect_view',
    ),
)
