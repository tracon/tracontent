from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracommon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='day',
            field=models.CharField(default='vkl', max_length=3),
        ),
    ]
