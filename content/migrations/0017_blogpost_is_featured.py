from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_sitesettings_context_processor_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Korostetut postaukset n\xe4kyv\xe4t sit\xe4 tukevilla sivustoilla n\xe4ytt\xe4v\xe4mmin.', verbose_name='Korosta postausta'),
        ),
    ]
