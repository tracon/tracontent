# encoding: utf-8

from django.shortcuts import get_object_or_404, redirect

from .models import BannerClick, Banner


def ads_banner_redirect_view(request, banner_id):
    banner = get_object_or_404(Banner, site=request.site, id=int(banner_id))

    if not request.user.is_staff:
        BannerClick.click(banner)

    return redirect(banner.url)
