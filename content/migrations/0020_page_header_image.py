from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_auto_20160511_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='header_image',
            field=models.FileField(blank=True, upload_to='headers'),
        ),
    ]
