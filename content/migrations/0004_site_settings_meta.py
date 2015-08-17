# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='description',
            field=models.TextField(default=b'', help_text='N\xe4kyy mm. hakukoneille sek\xe4 RSS-asiakasohjelmille.', verbose_name='Sivuston kuvaus', blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='keywords',
            field=models.TextField(default=b'', help_text='Pilkuilla erotettu avainsanalista. N\xe4kyy mm. hakukoneille.', verbose_name='Sivuston avainsanat', blank=True),
        ),
    ]
