# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermeta',
            options={'verbose_name': 'K\xe4ytt\xe4j\xe4n lis\xe4tiedot', 'verbose_name_plural': 'K\xe4ytt\xe4jien lis\xe4tiedot'},
        ),
    ]
