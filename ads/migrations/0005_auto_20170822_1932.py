from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_auto_20160511_2048'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bannerclick',
            unique_together=set([('site', 'banner', 'date')]),
        ),
    ]
