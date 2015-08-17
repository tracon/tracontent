# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_blog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ('-date', '-public_from'), 'verbose_name': 'blogipostaus', 'verbose_name_plural': 'blogipostaukset'},
        ),
    ]
