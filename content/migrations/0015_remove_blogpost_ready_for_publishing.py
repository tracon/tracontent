from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_blogpost_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='ready_for_publishing',
        ),
    ]
