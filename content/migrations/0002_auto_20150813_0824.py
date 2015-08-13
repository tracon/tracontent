# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'verbose_name': 'blogipostaus', 'verbose_name_plural': 'blogipostaukset'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'sivu', 'verbose_name_plural': 'sivut'},
        ),
        migrations.AlterModelOptions(
            name='redirect',
            options={'verbose_name': 'uudelleenohjaus', 'verbose_name_plural': 'uudelleenohjaukset'},
        ),
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(related_name='child_page_set', blank=True, to='content.Page', help_text='Jos valitset t\xe4h\xe4n sivun, t\xe4m\xe4 sivu luodaan valitun sivun alaisuuteen. Jos j\xe4t\xe4t t\xe4m\xe4n tyhj\xe4ksi, sivu luodaan p\xe4\xe4tasolle.', null=True, verbose_name='Yl\xe4sivu'),
        ),
    ]
