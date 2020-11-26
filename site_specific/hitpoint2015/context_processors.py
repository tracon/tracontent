from django.utils.timezone import now

from content.models import MenuEntry, Page


def hitpoint2015_context(request):
    site_settings = request.site.site_settings
    t = now()

    if request.path.startswith('/blog') or request.path.startswith('/fi'):
        subsite_path = 'fi'
    elif request.path.startswith('/en'):
        subsite_path = 'en'
    else:
        subsite_path = None

    if subsite_path:
        subsite_frontpage = Page.objects.get(site=request.site, path=subsite_path)
        menu = site_settings.get_menu(t=t, parent=subsite_frontpage, current_url=request.path)
        subsite_frontpage = subsite_frontpage.get_menu_entry(t=t)
    else:
        subsite_frontpage = None
        menu = []

    return dict(
        subsite_frontpage=subsite_frontpage,
        menu=menu,
    )
