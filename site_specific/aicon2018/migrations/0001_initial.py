from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.FileField(blank=True, null=True, upload_to='organizers', verbose_name='Naamakuva')),
                ('first_name', models.CharField(max_length=127, verbose_name='Etunimi')),
                ('last_name', models.CharField(blank=True, max_length=127, verbose_name='Sukunimi')),
                ('nick', models.CharField(blank=True, max_length=127, verbose_name='Nick')),
                ('job_title', models.CharField(blank=True, max_length=127, verbose_name='Tehtävä')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Sähköpostiosoite')),
                ('order', models.IntegerField(default=0, help_text='Pienin ensin, samannumeroiset sukunimen mukaan', verbose_name='Järjestys')),
            ],
            options={
                'verbose_name': 'Järjestäjä',
                'verbose_name_plural': 'Järjestäjät',
                'ordering': ('order', 'last_name', 'first_name'),
            },
        ),
    ]
