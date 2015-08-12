from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^(?P<path>[a-z0-9-/]+)', include('kompassi_oauth2.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('content.urls')),
)
