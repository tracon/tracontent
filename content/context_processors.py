def content_context(request):
    from django.conf import settings
    from django.contrib.sites.shortcuts import get_current_site

    site = get_current_site(request)

    vars = dict(
        site=site,
        site_settings=site.sitesettings,
        settings=settings,
    )

    return vars
