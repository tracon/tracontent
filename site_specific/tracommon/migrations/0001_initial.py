from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('homepage_url', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('image_file', models.ImageField(blank=True, upload_to='artists')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'taiteilija',
                'verbose_name_plural': 'taiteilijat',
                'ordering': ('site', 'table_number', 'name'),
            },
        ),
    ]
