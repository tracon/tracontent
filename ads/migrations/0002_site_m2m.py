from django.db import models, migrations


def migrate_site_m2m(apps, schema_editor):
    Banner = apps.get_model('ads', 'banner')
    BannerClick = apps.get_model('ads', 'bannerclick')

    for banner in Banner.objects.all():
        banner.sites.set([banner.site])
        banner.save()

    for banner_click in BannerClick.objects.all():
        banner_click.site = banner_click.banner.site
        banner_click.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='sites',
            field=models.ManyToManyField(related_name='+', verbose_name='Sivustot', to='sites.Site'),
        ),
        migrations.AddField(
            model_name='bannerclick',
            name='site',
            field=models.ForeignKey(verbose_name='Sivusto', to='sites.Site', null=True, on_delete=models.CASCADE),
        ),
        migrations.RunPython(migrate_site_m2m),
        migrations.RemoveField(
            model_name='banner',
            name='site',
        ),
        migrations.AlterField(
            model_name='banner',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='Sivustot'),
        ),
    ]
