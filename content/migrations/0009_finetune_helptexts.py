from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_delegate_site_title_to_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='author_ip_address',
            field=models.CharField(help_text='IP-osoite n\xe4kyy vain yll\xe4pitok\xe4ytt\xf6liittym\xe4ss\xe4.', max_length=17, verbose_name='IP-osoite', blank=True),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='removed_at',
            field=models.DateTimeField(null=True, verbose_name='Piilottamisaika', blank=True),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='removed_by',
            field=models.ForeignKey(verbose_name='Piilottaja', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL),
        ),
    ]
