from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_sitesettings_google_analytics_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='override_page_template',
            field=models.CharField(default='', help_text='Sivut n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Sivupohja', blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='page_controller_code',
            field=models.CharField(default='', help_text='Polku funktioon, joka suoritetaan joka sivulatauksella ja joka voi m\xe4\xe4ritell\xe4 lis\xe4\xe4 muuttujia sivupohjan nimiavaruuteen.', max_length=255, verbose_name='Sivukontrolleri', blank=True),
        ),
    ]
