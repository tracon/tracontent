from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_blogpost_is_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(help_text='Voit halutessasi lis\xe4t\xe4 postauksen yhteen tai useampaan kategoriaan. Kaikkien valittujen kategorioiden tulee olla samalla sivustolla postauksen kanssa.', related_name='blog_posts', verbose_name='Kategoriat', to='content.BlogCategory', blank=True),
        ),
    ]
