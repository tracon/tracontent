# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-22 16:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_auto_20160511_2048'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bannerclick',
            unique_together=set([('site', 'banner', 'date')]),
        ),
    ]
