# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(help_text='Lempi- tai kutsumanimi', max_length=1023, blank=True)),
                ('preferred_name_display_style', models.CharField(blank=True, help_text='T\xe4ss\xe4 voit vaikuttaa siihen, miss\xe4 muodossa nimesi esitet\xe4\xe4n (esim. painetaan badgeesi).', max_length=31, verbose_name='Nimen esitt\xe4minen', choices=[('firstname_nick_surname', 'Etunimi "Nick" Sukunimi'), ('firstname_surname', 'Etunimi Sukunimi'), ('firstname', 'Etunimi'), ('nick', 'Nick')])),
                ('user', models.OneToOneField(verbose_name='K\xe4ytt\xe4j\xe4', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
