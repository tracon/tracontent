# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_finetune_helptexts'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='google_analytics_token',
            field=models.CharField(help_text='Jos t\xe4yt\xe4t t\xe4h\xe4n Google Analytics -sivustoavaimen, ei-kirjautuneiden k\xe4ytt\xe4jien visiitit raportoidaan Google Analyticsiin.', max_length=63, verbose_name='Google Analytics -avain', blank=True),
        ),
    ]
