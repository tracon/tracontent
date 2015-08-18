# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_blog_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcomment',
            options={'ordering': ('created_at',), 'verbose_name': 'blogikommentti', 'verbose_name_plural': 'blogikommentit'},
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='author_email',
            field=models.EmailField(help_text='S\xe4hk\xf6postiosoitetta ei julkaista.', max_length=254, verbose_name='S\xe4hk\xf6postiosoite'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='author_name',
            field=models.CharField(help_text='N\xe4kyy muille sivun lukijoille.', max_length=1023, verbose_name='Nimi tai nimimerkki'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='comment',
            field=models.TextField(help_text='Pidet\xe4\xe4n keskustelu yst\xe4v\xe4llisen\xe4, asiallisena ja muita kunnioittavana. Yll\xe4pito poistaa asiattomat kommentit.', verbose_name='Kommentti'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Luotu'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Luotu'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='P\xe4ivitetty'),
        ),
        migrations.AlterField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Luotu'),
        ),
        migrations.AlterField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='P\xe4ivitetty'),
        ),
    ]
