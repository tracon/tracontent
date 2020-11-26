
from .views import resources_style_sheet_view
from django.urls import re_path


urlpatterns = [
    re_path(r'^css/(?P<style_sheet_name>[a-z0-9_\.]+)$',
        resources_style_sheet_view,
        name='resources_style_sheet_view',
    ),
]
