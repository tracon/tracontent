from .models import Banner


def ads_context(request):
    return dict(
        banners=Banner.objects.filter(site=request.site, active=True).order_by('?')
    )
