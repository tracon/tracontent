
from .views import ads_banner_redirect_view
from django.urls import re_path


urlpatterns = [
    re_path(r'^banners/(?P<banner_id>\d+)/redirect/?$',
        ads_banner_redirect_view,
        name='ads_banner_redirect_view',
    ),
]
