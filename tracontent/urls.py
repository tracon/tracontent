from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from .views import logout_view


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^logout/?', logout_view, name='logout_view'),
]


if 'kompassi_oauth2' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'', include('kompassi_oauth2.urls')))

if 'ads' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'', include('ads.urls')))

if 'resources' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'', include('resources.urls')))

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


# This needs to come last due to a catch-all route
urlpatterns.append(url(r'', include('content.urls')))
