from datetime import date

from django.test import TransactionTestCase, Client

from content.models import SiteSettings

from .models import Banner, BannerClick


class AdClickTestCase(TransactionTestCase):
    def setUp(self):
        self.site_settings, unused = SiteSettings.get_or_create_dummy()
        self.site = self.site_settings.site
        self.banner, unused = Banner.get_or_create_dummy()

    def test_banner_click(self):
        self.assertFalse(self.banner.banner_click_set.exists())

        d1 = date(2015, 8, 17)

        BannerClick.click(self.site, self.banner, d=d1)
        BannerClick.click(self.site, self.banner, d=d1)

        self.assertEqual(self.banner.banner_click_set.get(date=d1).clicks, 2)

        d2 = date(2015, 8, 18)

        BannerClick.click(self.site, self.banner, d=d2)

        self.assertEqual(self.banner.banner_click_set.count(), 2)
        self.assertEqual(self.banner.banner_click_set.get(date=d1).clicks, 2)
        self.assertEqual(self.banner.banner_click_set.get(date=d2).clicks, 1)
