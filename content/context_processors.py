from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now

from .utils import get_code

def content_context(request):
    site_settings = request.site.site_settings
    menu = site_settings.get_menu(t=now(), current_url=request.path)

    app_name = (
        'TraContent CMS Enterprise Edition'
        if 'kompassi_oauth2' in settings.INSTALLED_APPS
        else 'TraContent CMS Standard Edition'
    )

    vars = dict(
        site=request.site,
        site_settings=site_settings,
        menu=menu,
        settings=settings,
        feeds=dict(
            rss=request.build_absolute_uri(reverse('content_blog_feed_rss_view')),
            atom=request.build_absolute_uri(reverse('content_blog_feed_atom_view')),
        ),
        tracontent_app_name=app_name,
        tracontent_footer=u"<a href='https://github.com/tracon/tracontent' target='_blank'>{app_name}"
            "</a> © 2014–2018 <a href='https://github.com/tracon/tracontent/blob/master/LICENSE'>"
            "Santtu Pajukanta</a>.".format(app_name=app_name)
    )


    if site_settings.context_processor_code:
        context_processor_func = get_code(site_settings.context_processor_code)
        vars.update(context_processor_func(request))

    return vars
