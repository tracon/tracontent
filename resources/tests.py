
from django.test import TestCase, Client
from django.template.loader import get_template

from content.models import SiteSettings

from .models import Template, StyleSheet


class CodeResourceTestCase(TestCase):
    def setUp(self):
        self.site_settings, unused = SiteSettings.get_or_create_dummy()
        self.site = self.site_settings.site

        self.client = Client(HTTP_HOST=self.site.domain)

    def test_template_loader(self):
        db_template = Template.objects.create(name='foo.html', content='<h1>Hello, World!</h1>')
        dj_template = get_template('foo.html')

        self.assertEqual(db_template.content, dj_template.render({}))

    def test_style_sheet(self):
        style_sheet = StyleSheet.objects.create(name='foo.css', content='h1 { color: red }')

        response = self.client.get('/css/foo.css')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/css')
        self.assertEqual(response.content, style_sheet.content)
