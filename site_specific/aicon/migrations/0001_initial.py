# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_file', models.FileField(upload_to=b'organizers', null=True, verbose_name='Naamakuva', blank=True)),
                ('first_name', models.CharField(max_length=127, verbose_name='Etunimi')),
                ('last_name', models.CharField(max_length=127, verbose_name='Sukunimi', blank=True)),
                ('nick', models.CharField(max_length=127, verbose_name='Nick', blank=True)),
                ('job_title', models.CharField(max_length=127, verbose_name='Teht\xe4v\xe4', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='S\xe4hk\xf6postiosoite', blank=True)),
                ('order', models.IntegerField(default=0, help_text='Pienin ensin, samannumeroiset sukunimen mukaan', verbose_name='J\xe4rjestys')),
            ],
            options={
                'ordering': ('order', 'last_name', 'first_name'),
                'verbose_name': 'J\xe4rjest\xe4j\xe4',
                'verbose_name_plural': 'J\xe4rjest\xe4j\xe4t',
            },
        ),
    ]
