from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_auto_20160218_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='active',
            field=models.BooleanField(default=True, help_text='Voit piilottaa bannerin poistamatta sitä ottamalla tästä ruksin pois.', verbose_name='Aktiivinen'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_file',
            field=models.FileField(upload_to='banners'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(help_text='Esimerkiksi mainostettavan yrityksen tai sivuston nimi. Näytetään alt- ja hover-tekstinä.', max_length=1023, verbose_name='Otsikko'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(help_text='Bannerin klikkaaja ohjataan tähän osoitteeseen.', max_length=1023, verbose_name='Osoite'),
        ),
        migrations.AlterField(
            model_name='bannerclick',
            name='date',
            field=models.DateField(verbose_name='Päivämäärä'),
        ),
    ]
