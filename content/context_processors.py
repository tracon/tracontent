# encoding: utf-8

from django.utils.timezone import now


def content_context(request):
    from django.conf import settings
    from django.contrib.sites.shortcuts import get_current_site

    site = get_current_site(request)
    site_settings = site.sitesettings
    menu = site_settings.get_menu(t=now(), current_url=request.path)

    vars = dict(
        site=site,
        site_settings=site_settings,
        menu=menu,
        settings=settings,
        tracontent_footer=u"<a href='https://github.com/tracon/tracontent' target='_blank'>{app_name}"
          u"</a> © 2015 <a href='https://github.com/tracon/tracontent/blob/master/LICENSE'>"
          "Santtu Pajukanta</a>.".format(
            app_name=(
                'TraContent CMS Enterprise Edition'
                if 'kompassi_oauth2' in settings.INSTALLED_APPS
                else 'TraContent CMS Standard Edition'
            ),
        ),
    )

    return vars
