# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_blogpost_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='blog_post_template',
            field=models.CharField(default='example_blog_post.jade', help_text='Blogipostaukset n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Blogipostauspohja'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(help_text='P\xe4iv\xe4m\xe4\xe4r\xe4 on osa postauksen osoitetta. \xc4l\xe4 muuta p\xe4iv\xe4m\xe4\xe4r\xe4\xe4 julkaisun j\xe4lkeen. Jos j\xe4t\xe4t kent\xe4n tyhj\xe4ksi, siihen valitaan t\xe4m\xe4 p\xe4iv\xe4.', verbose_name='P\xe4iv\xe4m\xe4\xe4r\xe4', blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Jos j\xe4t\xe4t teknisen nimen tyhj\xe4ksi, se generoidaan automaattisesti otsikosta. Jos muutat teknist\xe4 nime\xe4 julkaisun j\xe4lkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')]),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Jos j\xe4t\xe4t teknisen nimen tyhj\xe4ksi, se generoidaan automaattisesti otsikosta. Jos muutat teknist\xe4 nime\xe4 julkaisun j\xe4lkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')]),
        ),
    ]
