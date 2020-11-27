from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from .views import logout_view, status_view
from django.urls import path, re_path


admin.autodiscover()

urlpatterns = []

# Disable Django Admin login view and use OAuth2 to Kompassi instead
if 'kompassi_oauth2' in settings.INSTALLED_APPS and not settings.DEBUG:
    from kompassi_oauth2.views import LoginView

    urlpatterns.append(re_path(r'^admin/login/?$', LoginView.as_view()))

urlpatterns.extend((
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^logout/?$', logout_view, name='logout_view'),
    re_path(r'^api/v1/status/?$', status_view, name='status_view'),
))


if 'kompassi_oauth2' in settings.INSTALLED_APPS:
    urlpatterns.append(re_path(r'', include('kompassi_oauth2.urls')))

if 'ads' in settings.INSTALLED_APPS:
    urlpatterns.append(re_path(r'', include('ads.urls')))

if 'resources' in settings.INSTALLED_APPS:
    urlpatterns.append(re_path(r'', include('resources.urls')))

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


# This needs to come last due to a catch-all route
urlpatterns.append(re_path(r'', include('content.urls')))
