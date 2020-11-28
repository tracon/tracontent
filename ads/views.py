from django.shortcuts import get_object_or_404, redirect

from .models import BannerClick, Banner


def ads_banner_redirect_view(request, banner_id):
    banner = get_object_or_404(Banner, sites=request.site, id=int(banner_id))

    if not request.user.is_staff:
        BannerClick.click(request.site, banner)

    return redirect(banner.url)
