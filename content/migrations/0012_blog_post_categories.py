# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('content', '0011_page_controller'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Jos j\xe4t\xe4t teknisen nimen tyhj\xe4ksi, se generoidaan automaattisesti otsikosta. Jos muutat teknist\xe4 nime\xe4 julkaisun j\xe4lkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('title', models.CharField(help_text='Otsikko n\xe4ytet\xe4\xe4n automaattisesti sivun yl\xe4laidassa sek\xe4 valikossa. \xc4l\xe4 lis\xe4\xe4 erillist\xe4 p\xe4\xe4otsikkoa sivun tekstiin.', max_length=1023, verbose_name='Otsikko')),
                ('site', models.ForeignKey(verbose_name='Sivusto', to='sites.Site')),
            ],
            options={
                'verbose_name': 'Blogin kategoria',
                'verbose_name_plural': 'Blogin kategoriat',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(related_name='blog_posts', verbose_name='Kategoriat', to='content.BlogCategory', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='blogcategory',
            unique_together=set([('site', 'slug')]),
        ),
    ]
