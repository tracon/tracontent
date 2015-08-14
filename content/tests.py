from django.test import TestCase

from .models import Page, SiteSettings


class PageTestCase(TestCase):
	def setUp(self):
		self.site_settings, unused = SiteSettings.get_or_create_dummy()
		self.site = self.site_settings.site

	def test_child_page_path(self):
		parent_page = Page(site=self.site, slug='parent', title='parent')
		parent_page.save()

		self.assertEqual(parent_page, Page.objects.get(path='parent'))

		child_page = Page(site=self.site, parent=parent_page, slug='child', title='child')
		child_page.save()

		self.assertEqual(child_page, Page.objects.get(path='parent/child'))