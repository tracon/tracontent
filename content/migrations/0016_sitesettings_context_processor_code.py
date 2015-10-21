# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_remove_blogpost_ready_for_publishing'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='context_processor_code',
            field=models.CharField(default='', help_text='Polku funktioon, joka suoritetaan joka sivulatauksella ja joka voi m\xe4\xe4ritell\xe4 lis\xe4\xe4 muuttujia sivuston nimiavaruuteen.', max_length=255, verbose_name='Sivustokontrolleri', blank=True),
        ),
    ]
