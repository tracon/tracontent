from django.db import models, migrations


def populate_site_name(apps, schema_editor):
    SiteSettings = apps.get_model('content', 'sitesettings')

    for site_settings in SiteSettings.objects.all():
        if not site_settings.site.name:
            site_settings.site.name = site_settings.title


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_misc'),
    ]

    operations = [
        migrations.RunPython(populate_site_name),
        migrations.RemoveField(
            model_name='sitesettings',
            name='title',
        ),
    ]
