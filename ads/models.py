# encoding: utf-8

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models, transaction, IntegrityError
from django.db.models import F
from django.utils.timezone import now


class Banner(models.Model):
    site = models.ForeignKey(Site, verbose_name=u'Sivusto')

    title = models.CharField(
        max_length=1023,
        verbose_name=u'Otsikko',
        help_text=u'Esimerkiksi mainostettavan yrityksen tai sivuston nimi. Näytetään alt- ja hover-tekstinä.',
    )

    url = models.CharField(
        max_length=1023,
        verbose_name=u'Osoite',
        help_text=u'Bannerin klikkaaja ohjataan tähän osoitteeseen.',
    )

    image_file = models.FileField(
        upload_to='banners',

    )

    active = models.BooleanField(
        default=True,
        verbose_name=u'Aktiivinen',
        help_text=u'Voit piilottaa bannerin poistamatta sitä ottamalla tästä ruksin pois.'
    )

    @classmethod
    def get_or_create_dummy(cls):
        from content.models import SiteSettings
        site_settings, unused = SiteSettings.get_or_create_dummy()

        return cls.objects.get_or_create(
            site=site_settings.site,
            title='Dummy banner',
            url='http://example.com',
            image_file='dummy.jpg',
        )

    def get_absolute_url(self):
        return reverse('ads_banner_redirect_view', args=(self.pk,))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'banneri'
        verbose_name_plural = u'bannerit'


class BannerClick(models.Model):
    banner = models.ForeignKey(Banner,
        verbose_name=u'Banneri',
        related_name='banner_click_set'
    )

    date = models.DateField(verbose_name=u'Päivämäärä')
    clicks = models.IntegerField(verbose_name=u'Klikkauksia')

    @classmethod
    def click(cls, banner, d=None):
        if d is None:
            d = now().date()

        with transaction.atomic():
            banner_click, created = BannerClick.objects.select_for_update().get_or_create(
                banner=banner,
                date=d,
                defaults=dict(
                    clicks=1,
                ),
            )
            if not created:
                banner_click.clicks = F('clicks') + 1
                banner_click.save()

    @property
    def site(self):
        return self.banner.site

    def __unicode__(self):
        return u"{banner_title} ({date})".format(
            banner_title=self.banner.title if self.banner else None,
            date=self.date.isoformat() if self.date else None,
        )

    class Meta:
        unique_together = [('banner', 'date')]
        verbose_name = u'bannerin klikkaukset'
        verbose_name_plural = u'bannerien klikkaukset'
