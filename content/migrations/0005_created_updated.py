# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


MAGIC_DATETIME = datetime.datetime(2015, 8, 17, 9, 32, 48, 54124, tzinfo=utc)


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_site_settings_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created_at',
            field=models.DateTimeField(default=MAGIC_DATETIME, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='updated_at',
            field=models.DateTimeField(default=MAGIC_DATETIME, auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(default=MAGIC_DATETIME, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(default=MAGIC_DATETIME, auto_now=True),
            preserve_default=False,
        ),
    ]
