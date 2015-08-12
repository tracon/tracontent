# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('date', models.DateField()),
                ('slug', models.CharField(help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('public_from', models.DateTimeField(null=True, blank=True)),
                ('visible_from', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=1023)),
                ('body', models.TextField()),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('slug', models.CharField(blank=True, help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.', max_length=63, verbose_name='Tekninen nimi', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('public_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen my\xf6s sis\xe4\xe4nkirjautumattomien k\xe4ytt\xe4jien luettavissa, jos n\xe4m\xe4 tiet\xe4v\xe4t osoitteen.', null=True, verbose_name=b'Julkaisuaika', blank=True)),
                ('visible_from', models.DateTimeField(help_text='Sivu on t\xe4st\xe4 hetkest\xe4 alkaen n\xe4kyviss\xe4 valikossa.', null=True, verbose_name='N\xe4kyviss\xe4 valikossa alkaen', blank=True)),
                ('title', models.CharField(max_length=1023)),
                ('body', models.TextField()),
                ('parent', models.ForeignKey(blank=True, to='content.Page', null=True)),
                ('site', models.ForeignKey(verbose_name='Sivusto', to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text='Polku m\xe4\xe4ritet\xe4\xe4n automaattisesti teknisen nimen perusteella.', max_length=1023, verbose_name='Polku', validators=[django.core.validators.RegexValidator(regex=b'[a-z0-9-]+', message='Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.')])),
                ('target', models.CharField(max_length=1023)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
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
