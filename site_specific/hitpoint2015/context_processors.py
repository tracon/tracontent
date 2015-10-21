# encoding: utf-8

from django.utils.timezone import now

from content.models import MenuEntry


def hitpoint2015_context(request):
    site_settings = request.site.site_settings
    menu = site_settings.get_menu(t=now(), current_url=request.path)

    for subsite_path in ['/fi', '/en']:
      print 'request.path', request.path
      print 'subsite_path', subsite_path
      if request.path.startswith(subsite_path):
          subsite_frontpage = next(menu_entry for menu_entry in menu if menu_entry.href == subsite_path)
          print subsite_frontpage
          menu = subsite_frontpage.children
          break
      else:
          print 'aieee'
          subsite_frontpage = None

    return dict(
        subsite_frontpage=subsite_frontpage,
        menu=menu,
    )
