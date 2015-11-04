# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StyleSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Uniikki tunniste, jolla resurssi ladataan koodista tai HTML:st\xe4 k\xe4sin.', unique=True, max_length=63, verbose_name='Nimi')),
                ('active', models.BooleanField(default=True, help_text='Ei-aktiivisia resursseja ei huomioida.', verbose_name='Aktiivinen')),
                ('content', models.TextField(verbose_name='Sis\xe4lt\xf6', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Luotu')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Muokattu')),
            ],
            options={
                'verbose_name': 'Tyylitiedosto',
                'verbose_name_plural': 'Tyylitiedostot',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Uniikki tunniste, jolla resurssi ladataan koodista tai HTML:st\xe4 k\xe4sin.', unique=True, max_length=63, verbose_name='Nimi')),
                ('active', models.BooleanField(default=True, help_text='Ei-aktiivisia resursseja ei huomioida.', verbose_name='Aktiivinen')),
                ('content', models.TextField(verbose_name='Sis\xe4lt\xf6', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Luotu')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Muokattu')),
            ],
            options={
                'verbose_name': 'Sivupohja',
                'verbose_name_plural': 'Sivupohjat',
            },
        ),
    ]
