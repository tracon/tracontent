from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Esimerkiksi mainostettavan yrityksen tai sivuston nimi. N\xe4ytet\xe4\xe4n alt- ja hover-tekstin\xe4.', max_length=1023, verbose_name='Otsikko')),
                ('url', models.CharField(help_text='Bannerin klikkaaja ohjataan t\xe4h\xe4n osoitteeseen.', max_length=1023, verbose_name='Osoite')),
                ('image_file', models.FileField(upload_to=b'banners')),
                ('active', models.BooleanField(default=True, help_text='Voit piilottaa bannerin poistamatta sit\xe4 ottamalla t\xe4st\xe4 ruksin pois.', verbose_name='Aktiivinen')),
                ('site', models.ForeignKey(verbose_name='Sivusto', to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'banneri',
                'verbose_name_plural': 'bannerit',
            },
        ),
        migrations.CreateModel(
            name='BannerClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='P\xe4iv\xe4m\xe4\xe4r\xe4')),
                ('clicks', models.IntegerField(verbose_name='Klikkauksia')),
                ('banner', models.ForeignKey(related_name='banner_click_set', verbose_name='Banneri', to='ads.Banner', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'bannerin klikkaukset',
                'verbose_name_plural': 'bannerien klikkaukset',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bannerclick',
            unique_together=set([('banner', 'date')]),
        ),
    ]
