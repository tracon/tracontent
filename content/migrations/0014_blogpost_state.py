# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_ready_for_publishing_to_state(apps, schema_editor):
    BlogPost = apps.get_model('content', 'blogpost')
    BlogPost.objects.filter(ready_for_publishing=True).update(state='ready')
    BlogPost.objects.filter(ready_for_publishing=False).update(state='draft')


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_blog_post_internal_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='state',
            field=models.CharField(default=b'draft', help_text='T\xe4m\xe4 kentt\xe4 kommunikoi muille julkaisuj\xe4rjestelm\xe4n k\xe4ytt\xe4jille, onko sivu kirjoittajan mielest\xe4 valmis julkaistavaksi. Jos et itse julkaise kirjoitustasi, j\xe4t\xe4 kirjoituksesi tilaan "Odottaa tarkistusta" kun se on mielest\xe4si valmis. T\xe4m\xe4 kentt\xe4 ei vaikuta teknisesti kirjoituksen julkaisuun mill\xe4\xe4n tavalla.', max_length=7, verbose_name='Luonnoksen tila', choices=[(b'draft', 'Luonnos'), (b'review', 'Odottaa tarkistusta'), (b'ready', 'Valmis julkaistavaksi')]),
        ),
        migrations.RunPython(migrate_ready_for_publishing_to_state),
    ]
