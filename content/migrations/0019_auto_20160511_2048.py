import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20151209_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Jos jätät teknisen nimen tyhjäksi, se generoidaan automaattisesti otsikosta. Jos muutat teknistä nimeä julkaisun jälkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, validators=[django.core.validators.RegexValidator(message='Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.', regex='[a-z0-9-]+')], verbose_name='Tekninen nimi'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='override_excerpt',
            field=models.TextField(blank=True, default='', help_text='Kirjoita muutaman lauseen mittainen lyhennelmä kirjoituksesta. Lyhennelmä näkyy blogilistauksessa. Mikäli lyhennelmää ei ole annettu, leikataan lyhennelmäksi sopivan mittainen pätkä itse kirjoituksesta.', verbose_name='Lyhennelmä'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='path',
            field=models.CharField(help_text='Polku määritetään automaattisesti teknisen nimen perusteella.', max_length=1023, validators=[django.core.validators.RegexValidator(message='Polku saa sisältää vain pieniä kirjaimia, numeroita, väliviivoja sekä kauttaviivoja.', regex='[a-z0-9-/]+')], verbose_name='Polku'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Jos jätät teknisen nimen tyhjäksi, se generoidaan automaattisesti otsikosta. Jos muutat teknistä nimeä julkaisun jälkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, validators=[django.core.validators.RegexValidator(message='Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.', regex='[a-z0-9-]+')], verbose_name='Tekninen nimi'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='state',
            field=models.CharField(choices=[('draft', 'Luonnos'), ('review', 'Odottaa tarkistusta'), ('ready', 'Valmis julkaistavaksi')], default='draft', help_text='Tämä kenttä kommunikoi muille julkaisujärjestelmän käyttäjille, onko sivu kirjoittajan mielestä valmis julkaistavaksi. Jos et itse julkaise kirjoitustasi, jätä kirjoituksesi tilaan "Odottaa tarkistusta" kun se on mielestäsi valmis. Tämä kenttä ei vaikuta teknisesti kirjoituksen julkaisuun millään tavalla.', max_length=7, verbose_name='Luonnoksen tila'),
        ),
        migrations.AlterField(
            model_name='page',
            name='path',
            field=models.CharField(help_text='Polku määritetään automaattisesti teknisen nimen perusteella.', max_length=1023, validators=[django.core.validators.RegexValidator(message='Polku saa sisältää vain pieniä kirjaimia, numeroita, väliviivoja sekä kauttaviivoja.', regex='[a-z0-9-/]+')], verbose_name='Polku'),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(blank=True, help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Jos jätät teknisen nimen tyhjäksi, se generoidaan automaattisesti otsikosta. Jos muutat teknistä nimeä julkaisun jälkeen, muista luoda tarvittavat uudelleenojaukset.', max_length=63, validators=[django.core.validators.RegexValidator(message='Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.', regex='[a-z0-9-]+')], verbose_name='Tekninen nimi'),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='path',
            field=models.CharField(help_text='Polku määritetään automaattisesti teknisen nimen perusteella.', max_length=1023, validators=[django.core.validators.RegexValidator(message='Polku saa sisältää vain pieniä kirjaimia, numeroita, väliviivoja sekä kauttaviivoja.', regex='[a-z0-9-/]+')], verbose_name='Polku'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Näkyy mm. hakukoneille sekä RSS-asiakasohjelmille.', verbose_name='Sivuston kuvaus'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='keywords',
            field=models.TextField(blank=True, default='', help_text='Pilkuilla erotettu avainsanalista. Näkyy mm. hakukoneille.', verbose_name='Sivuston avainsanat'),
        ),
    ]
