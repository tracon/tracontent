from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import index_view, protected_view

urlpatterns = patterns('',
    url(r'', include('kompassi_oauth2.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.*/)$', 'django.contrib.flatpages.views.flatpage'),
)
