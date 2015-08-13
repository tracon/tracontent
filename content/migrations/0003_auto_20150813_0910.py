# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20150813_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='path',
            field=models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')]),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.CharField(help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')]),
        ),
        migrations.AlterField(
            model_name='page',
            name='path',
            field=models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')]),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')]),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='path',
            field=models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')]),
        ),
    ]
