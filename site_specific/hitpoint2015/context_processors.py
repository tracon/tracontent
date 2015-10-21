# encoding: utf-8

from django.utils.timezone import now

from content.models import MenuEntry


def hitpoint2015_context(request):
    site_settings = request.site.site_settings
    menu = site_settings.get_menu(t=now(), current_url=request.path)

    if request.path.startswith('/blog') or request.path.startswith('/fi'):
        subsite_path = '/fi'
    elif request.path.startswith('/en'):
        subsite_path = '/en'
    else:
        subsite_path = None

    if subsite_path:
        subsite_frontpage = next(menu_entry for menu_entry in menu if menu_entry.href == subsite_path)
        menu = subsite_frontpage.children
    else:
        subsite_frontpage = None
        menu = []

    return dict(
        subsite_frontpage=subsite_frontpage,
        menu=menu,
    )
