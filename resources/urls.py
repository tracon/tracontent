from django.conf.urls import patterns, include, url

from .views import resources_style_sheet_view


urlpatterns = patterns('',
    url(
        r'^css/(?P<style_sheet_name>[a-z0-9_\.]+)$',
        resources_style_sheet_view,
        name='resources_style_sheet_view',
    ),
)
