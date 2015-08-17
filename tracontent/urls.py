from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

actual_patterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
]

if 'kompassi_oauth2' in settings.INSTALLED_APPS:
    actual_patterns.append(
        url(r'', include('kompassi_oauth2.urls'))
    )

if 'ads' in settings.INSTALLED_APPS:
    actual_patterns.append(
        url(r'', include('ads.urls'))
    )

if settings.DEBUG:
    actual_patterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

# This needs to come last due to a catch-all route
actual_patterns.append(
    url(r'', include('content.urls')),
)

urlpatterns = patterns('', *actual_patterns)
