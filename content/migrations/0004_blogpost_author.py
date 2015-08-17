# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Jos j\xe4t\xe4t kent\xe4n tyhj\xe4ksi, tekij\xe4ksi asetetaan automaattisesti sinut.', null=True, verbose_name='Tekij\xe4'),
        ),
    ]
