from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')])),
                ('date', models.DateField(help_text='P\xe4iv\xe4m\xe4\xe4r\xe4 on osa postauksen osoitetta. \xc4l\xe4 muuta p\xe4iv\xe4m\xe4\xe4r\xe4\xe4 julkaisun j\xe4lkeen.', verbose_name='P\xe4iv\xe4m\xe4\xe4r\xe4')),
                ('slug', models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Jos j\xe4t\xe4t teknisen nimen tyhj\xe4ksi, se generoidaan automaattisesti otsikosta.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('public_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen my\xf6s sis\xe4\xe4nkirjautumattomien k\xe4ytt\xe4jien luettavissa, jos n\xe4m\xe4 tiet\xe4v\xe4t osoitteen. J\xe4t\xe4 tyhj\xe4ksi, jos haluat j\xe4tt\xe4\xe4 sivun luonnokseksi.', null=True, verbose_name='Julkaisuaika', blank=True)),
                ('visible_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen n\xe4kyviss\xe4 valikossa tai listauksessa. J\xe4t\xe4 tyhj\xe4ksi, jos haluat j\xe4tt\xe4\xe4 sivun piilotetuksi.', null=True, verbose_name='N\xe4kyviss\xe4 alkaen', blank=True)),
                ('title', models.CharField(help_text='Otsikko n\xe4ytet\xe4\xe4n automaattisesti sivun yl\xe4laidassa sek\xe4 valikossa. \xc4l\xe4 lis\xe4\xe4 erillist\xe4 p\xe4\xe4otsikkoa sivun tekstiin.', max_length=1023, verbose_name='Otsikko')),
                ('body', models.TextField(verbose_name='Leip\xe4teksti', blank=True)),
                ('site', models.ForeignKey(verbose_name='Sivusto', to='sites.Site', help_text='Sivusto, jolle t\xe4m\xe4 sivu kuuluu. HUOM! Kun haluat luoda saman sivun toiselle sivustolle, \xe4l\xe4 siirr\xe4 vanhaa sivua vaan k\xe4yt\xe4 sivunkopiointitoimintoa.', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'blogipostaus',
                'verbose_name_plural': 'blogipostaukset',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')])),
                ('slug', models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Jos j\xe4t\xe4t teknisen nimen tyhj\xe4ksi, se generoidaan automaattisesti otsikosta.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('public_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen my\xf6s sis\xe4\xe4nkirjautumattomien k\xe4ytt\xe4jien luettavissa, jos n\xe4m\xe4 tiet\xe4v\xe4t osoitteen. J\xe4t\xe4 tyhj\xe4ksi, jos haluat j\xe4tt\xe4\xe4 sivun luonnokseksi.', null=True, verbose_name='Julkaisuaika', blank=True)),
                ('visible_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen n\xe4kyviss\xe4 valikossa tai listauksessa. J\xe4t\xe4 tyhj\xe4ksi, jos haluat j\xe4tt\xe4\xe4 sivun piilotetuksi.', null=True, verbose_name='N\xe4kyviss\xe4 alkaen', blank=True)),
                ('title', models.CharField(help_text='Otsikko n\xe4ytet\xe4\xe4n automaattisesti sivun yl\xe4laidassa sek\xe4 valikossa. \xc4l\xe4 lis\xe4\xe4 erillist\xe4 p\xe4\xe4otsikkoa sivun tekstiin.', max_length=1023, verbose_name='Otsikko')),
                ('override_menu_text', models.CharField(help_text='Sivu n\xe4kyy t\xe4ll\xe4 nimell\xe4 valikossa. Jos j\xe4t\xe4t t\xe4m\xe4n tyhj\xe4ksi, k\xe4ytet\xe4\xe4n otsikkoa.', max_length=1023, verbose_name='Valikkoteksti', blank=True)),
                ('body', models.TextField(verbose_name='Leip\xe4teksti', blank=True)),
                ('parent', models.ForeignKey(related_name='child_page_set', blank=True, to='content.Page', help_text='Jos valitset t\xe4h\xe4n sivun, t\xe4m\xe4 sivu luodaan valitun sivun alaisuuteen. Jos j\xe4t\xe4t t\xe4m\xe4n tyhj\xe4ksi, sivu luodaan p\xe4\xe4tasolle.', null=True, verbose_name='Yl\xe4sivu', on_delete=models.CASCADE)),
                ('site', models.ForeignKey(verbose_name='Sivusto', to='sites.Site', help_text='Sivusto, jolle t\xe4m\xe4 sivu kuuluu. HUOM! Kun haluat luoda saman sivun toiselle sivustolle, \xe4l\xe4 siirr\xe4 vanhaa sivua vaan k\xe4yt\xe4 sivunkopiointitoimintoa.', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'sivu',
                'verbose_name_plural': 'sivut',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-/]+', message='Polku saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita, v\xe4liviivoja sek\xe4 kauttaviivoja.')])),
                ('target', models.CharField(max_length=1023)),
                ('site', models.ForeignKey(to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'uudelleenohjaus',
                'verbose_name_plural': 'uudelleenohjaukset',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Sivuston otsikko n\xe4kyy mm. selaimen v\xe4lilehden otsikossa.', max_length=1023, verbose_name='Sivuston otsikko')),
                ('base_template', models.CharField(help_text='Sivut n\xe4ytet\xe4\xe4n k\xe4ytt\xe4en t\xe4t\xe4 sivupohjaa. T\xe4m\xe4nnimisen sivupohjan tulee l\xf6yty\xe4 l\xe4hdekoodista.', max_length=127, verbose_name='Sivupohja')),
                ('site', models.OneToOneField(to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'sivustojen asetukset',
            },
        ),
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=set([('site', 'path')]),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('site', 'path'), ('site', 'parent', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='blogpost',
            unique_together=set([('site', 'path'), ('site', 'date', 'slug')]),
        ),
    ]
