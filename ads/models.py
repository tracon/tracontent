from django.contrib.sites.models import Site
from django.urls import reverse
from django.db import models, transaction, IntegrityError
from django.db.models import F
from django.utils.timezone import now


class Banner(models.Model):
    sites = models.ManyToManyField(Site, verbose_name='Sivustot')

    title = models.CharField(
        max_length=1023,
        verbose_name='Otsikko',
        help_text='Esimerkiksi mainostettavan yrityksen tai sivuston nimi. Näytetään alt- ja hover-tekstinä.',
    )

    url = models.CharField(
        max_length=1023,
        verbose_name='Osoite',
        help_text='Bannerin klikkaaja ohjataan tähän osoitteeseen.',
    )

    image_file = models.FileField(
        upload_to='banners',
    )

    active = models.BooleanField(
        default=True,
        verbose_name='Aktiivinen',
        help_text='Voit piilottaa bannerin poistamatta sitä ottamalla tästä ruksin pois.'
    )

    def admin_get_sites(self):
        return ', '.join(site.domain for site in self.sites.all())
    admin_get_sites.short_description = 'Sivustot'
    admin_get_sites.admin_order_field = 'sites'

    @classmethod
    def get_or_create_dummy(cls):
        from content.models import SiteSettings
        site_settings, unused = SiteSettings.get_or_create_dummy()

        obj, created = cls.objects.get_or_create(
            title='Dummy banner',
            url='http://example.com',
            image_file='dummy.jpg',
        )

        if created:
            obj.sites = [site_settings.site,]
            obj.save()

        return obj, created

    def get_absolute_url(self):
        return reverse('ads_banner_redirect_view', args=(self.pk,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'banneri'
        verbose_name_plural = 'bannerit'


class BannerClick(models.Model):
    site = models.ForeignKey(Site, verbose_name='Sivusto', null=True, on_delete=models.CASCADE)
    banner = models.ForeignKey(Banner,
        verbose_name='Banneri',
        related_name='banner_click_set',
        on_delete=models.CASCADE,
    )

    date = models.DateField(verbose_name='Päivämäärä')
    clicks = models.IntegerField(verbose_name='Klikkauksia')

    @classmethod
    def click(cls, site, banner, d=None):
        if d is None:
            d = now().date()

        with transaction.atomic():
            banner_click, created = BannerClick.objects.select_for_update().get_or_create(
                site=site,
                banner=banner,
                date=d,
                defaults=dict(
                    clicks=1,
                ),
            )
            if not created:
                banner_click.clicks = F('clicks') + 1
                banner_click.save()

    def __str__(self):
        return "{banner_title} ({date})".format(
            banner_title=self.banner.title if self.banner else None,
            date=self.date.isoformat() if self.date else None,
        )

    class Meta:
        unique_together = [('site', 'banner', 'date')]
        verbose_name = 'bannerin klikkaukset'
        verbose_name_plural = 'bannerien klikkaukset'
