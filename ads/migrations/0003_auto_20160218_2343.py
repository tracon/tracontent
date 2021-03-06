from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_site_m2m'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Voit piilottaa bannerin poistamatta sit\xc3\xa4 ottamalla t\xc3\xa4st\xc3\xa4 ruksin pois.', verbose_name=b'Aktiivinen'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(help_text=b'Esimerkiksi mainostettavan yrityksen tai sivuston nimi. N\xc3\xa4ytet\xc3\xa4\xc3\xa4n alt- ja hover-tekstin\xc3\xa4.', max_length=1023, verbose_name=b'Otsikko'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(help_text=b'Bannerin klikkaaja ohjataan t\xc3\xa4h\xc3\xa4n osoitteeseen.', max_length=1023, verbose_name=b'Osoite'),
        ),
        migrations.AlterField(
            model_name='bannerclick',
            name='date',
            field=models.DateField(verbose_name=b'P\xc3\xa4iv\xc3\xa4m\xc3\xa4\xc3\xa4r\xc3\xa4'),
        ),
    ]
