from django.conf.urls import patterns, include, url

from .views import public_view, protected_view


urlpatterns = patterns('',
    url(r'^$', public_view, name='public_view'),
    url(r'^protected$', protected_view, name='protected_view'),
)
