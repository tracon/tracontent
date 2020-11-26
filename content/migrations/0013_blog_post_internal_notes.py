from django.db import models, migrations


def set_ready_for_publishing_for_already_published_blog_posts(apps, schema_editor):
    BlogPost = apps.get_model('content', 'blogpost')
    BlogPost.objects.filter(visible_from__isnull=False).update(ready_for_publishing=True)


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_blog_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='internal_notes',
            field=models.TextField(help_text='T\xe4h\xe4n kentt\xe4\xe4n voit j\xe4tt\xe4\xe4 muistiinpanoja itsellesi ja muille julkaisuj\xe4rjestelm\xe4n k\xe4ytt\xe4jille esimerkiksi suunnittelemastasi sis\xe4ll\xf6st\xe4 tai kirjoituksen julkaisuaikataulusta. N\xe4m\xe4 muistiinpanot eiv\xe4t n\xe4y ulosp\xe4in, vaan ne on tarkoitettu puhtaasti julkaisuj\xe4rjestelm\xe4n toimittaja- ja yll\xe4pitok\xe4ytt\xe4jien tiedoksi.', verbose_name='Sis\xe4iset muistiinpanot', blank=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='ready_for_publishing',
            field=models.BooleanField(default=False, help_text='T\xe4m\xe4 kentt\xe4 kommunikoi muille julkaisuj\xe4rjestelm\xe4n k\xe4ytt\xe4jille, onko sivu kirjoittajan mielest\xe4 valmis julkaistavaksi. Jos et itse julkaise kirjoitustasi, ruksaa t\xe4m\xe4 kentt\xe4 kun luonnos on mielest\xe4si valmis. T\xe4m\xe4n kent\xe4n ruksaaminen ei yksin viel\xe4 julkaise kirjoitusta, vaan julkaisua kontrolloivat alla olevat julkaisu- ja n\xe4kyvyyskent\xe4t, eik\xe4 t\xe4m\xe4n kent\xe4n tarvitse olla ruksattuna jotta kirjoituksen voisi teknisesti julkaista niiden avulla.', verbose_name='Valmis julkaistavaksi'),
        ),
        migrations.RunPython(set_ready_for_publishing_for_already_published_blog_posts)
    ]
