from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0005_created_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_name', models.CharField(max_length=1023)),
                ('author_email', models.EmailField(max_length=254)),
                ('author_ip_address', models.CharField(max_length=17, blank=True)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('removed_at', models.DateTimeField(null=True, blank=True)),
                ('blog_post', models.ForeignKey(related_name='blog_comment_set', verbose_name='Blogipostaus', to='content.BlogPost', on_delete=models.CASCADE)),
                ('removed_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'blogikommentti',
                'verbose_name_plural': 'blogikommentit',
            },
        ),
        migrations.AlterIndexTogether(
            name='blogcomment',
            index_together=set([('blog_post', 'removed_at')]),
        ),
    ]
