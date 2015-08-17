# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_page_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='page_template',
            field=models.CharField(default='example_page.jade', help_text='Sivut n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Sivupohja'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='order',
            field=models.IntegerField(default=0, help_text='Saman yl\xe4sivun alaiset sivut j\xe4rjestet\xe4\xe4n valikossa t\xe4m\xe4n luvun mukaan nousevaan j\xe4rjestykseen (pienin ensin).', verbose_name='J\xe4rjestys'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='base_template',
            field=models.CharField(help_text='Asettelupohja m\xe4\xe4rittelee sivuston perusasettelun. T\xe4m\xe4nnimisen asettelupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Asettelupohja'),
        ),
    ]
