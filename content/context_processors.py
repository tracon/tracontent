# encoding: utf-8

def content_context(request):
    from django.conf import settings
    from django.contrib.sites.shortcuts import get_current_site

    site = get_current_site(request)

    vars = dict(
        site=site,
        site_settings=site.sitesettings,
        settings=settings,
        tracontent_footer=u"<a href='https://github.com/tracon/tracontent' target='_blank'>TraContent "
          u"CMS Enterprise Edition</a> © 2015 <a href='https://github.com/tracon/tracontent/blob/master/LICENSE'>"
          "Santtu Pajukanta</a>.",
    )

    return vars
