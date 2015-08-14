from django.test import TestCase, Client
from django.utils.timezone import now

from .models import Page, SiteSettings


class PageTestCase(TestCase):
	def setUp(self):
		self.site_settings, unused = SiteSettings.get_or_create_dummy()
		self.site = self.site_settings.site

		self.client = Client(HTTP_HOST=self.site.domain)

	def test_child_page_path(self):
		parent_page = Page(site=self.site, slug='parent', title='parent')
		parent_page.save()

		self.assertEqual(parent_page, Page.objects.get(path='parent'))

		child_page = Page(site=self.site, parent=parent_page, slug='child', title='child')
		child_page.save()

		self.assertEqual(child_page, Page.objects.get(path='parent/child'))

	def test_public_from(self):
		page = Page(site=self.site, slug='foobar', title='foobar')
		page.save()

		# page not public yet
		response = self.client.get('/foobar')
		self.assertEqual(response.status_code, 404)

		page.public_from = now()
		page.save()

		response = self.client.get('/foobar')
		self.assertEqual(response.status_code, 200)

	def test_visible_from(self):
		page = Page(site=self.site, slug='foobar', title='foobar')
		page.save()

		# page not visible yet
		self.assertFalse(any(entry.href == '/foobar' for entry in self.site_settings.get_menu(t=now())))

		page.visible_from = now()
		page.save()

		self.assertTrue(any(entry.href == '/foobar' for entry in self.site_settings.get_menu(t=now())))