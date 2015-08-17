# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_page_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ('date', 'public_from'), 'verbose_name': 'blogipostaus', 'verbose_name_plural': 'blogipostaukset'},
        ),
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'sivuston asetukset', 'verbose_name_plural': 'sivustojen asetukset'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='override_excerpt',
            field=models.TextField(default=b'', help_text='Kirjoita muutaman lauseen mittainen lyhennelm\xe4 kirjoituksesta. Lyhennelm\xe4 n\xe4kyy blogilistauksessa. Mik\xe4li lyhennelm\xe4\xe4 ei ole annettu, leikataan lyhennelm\xe4ksi sopivan mittainen p\xe4tk\xe4 itse kirjoituksesta.', verbose_name='Lyhennelm\xe4', blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='blog_index_template',
            field=models.CharField(default='example_blog_index.jade', help_text='Blogilistaus n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Blogilistauspohja'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='page_template',
            field=models.CharField(default='example_page_template.jade', help_text='Sivut n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Sivupohja'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='site',
            field=models.ForeignKey(related_name='blog_post_set', verbose_name='Sivusto', to='sites.Site', help_text='Sivusto, jolle t\xe4m\xe4 sivu kuuluu. HUOM! Kun haluat luoda saman sivun toiselle sivustolle, \xe4l\xe4 siirr\xe4 vanhaa sivua vaan k\xe4yt\xe4 sivunkopiointitoimintoa.'),
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
        migrations.AlterField(
            model_name='sitesettings',
            name='site',
            field=models.OneToOneField(related_name='site_settings', verbose_name='Sivusto', to='sites.Site'),
        ),
    ]
