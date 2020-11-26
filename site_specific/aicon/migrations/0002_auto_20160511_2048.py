from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aicon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='organizers', verbose_name='Naamakuva'),
        ),
    ]
