from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('order',), 'verbose_name': 'sivu', 'verbose_name_plural': 'sivut'},
        ),
        migrations.AddField(
            model_name='page',
            name='order',
            field=models.IntegerField(default=0, help_text='Saman yl\xe4sivun alaiset sivut j\xe4rjestet\xe4\xe4n t\xe4m\xe4n luvun mukaan nousevaan j\xe4rjestykseen (pienin ensin).', verbose_name='J\xe4rjestys'),
        ),
    ]
