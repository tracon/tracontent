# encoding: utf-8

from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models


validate_slug = RegexValidator(
    regex=r'[a-z0-9-]+',
    message=u'Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.'
)
SLUG_FIELD_PARAMS = dict(
    max_length=63,
    validators=[validate_slug],
    verbose_name=u'Tekninen nimi',
    help_text=u'Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
        u'merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi '
        u'muuttaa luomisen jälkeen.',
)


validate_path = RegexValidator(
    regex=r'[a-z0-9-]+',
    message=u'Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.'
)
PATH_FIELD_PARAMS = dict(
    max_length=1023,
    validators=[validate_path],
    verbose_name=u'Polku',
    help_text=u'Polku määritetään automaattisesti teknisen nimen perusteella.',
)


class Page(models.Model):
    site = models.ForeignKey(Site, verbose_name=u'Sivusto')
    path = models.CharField(**PATH_FIELD_PARAMS)
    parent = models.ForeignKey('Page', null=True, blank=True)
    slug = models.CharField(blank=True, **SLUG_FIELD_PARAMS)

    public_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Julkaisuaika',
        help_text=u'Sivu on tästä hetkestä alkaen myös sisäänkirjautumattomien käyttäjien luettavissa, jos nämä tietävät osoitteen.',

    )
    visible_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Näkyvissä valikossa alkaen',
        help_text=u'Sivu on tästä hetkestä alkaen näkyvissä valikossa.',

    )

    title = models.CharField(max_length=1023)
    body = models.TextField()

    def _make_path(self):
        if self.parent is None:
            return self.slug
        else:
            return self.parent.path + '/' + self.path

    def save(self, *args, **kwargs):
        if self.slug:
            self.path = self._make_path()

        return super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{domain}/{path}'.format(
            domain=self.site.domain if self.site is not None else None,
            path=self.path,
        )

    class Meta:
        unique_together = [('site', 'path'), ('site', 'parent', 'slug')]


class Redirect(models.Model):
    site = models.ForeignKey(Site)
    path = models.CharField(**PATH_FIELD_PARAMS)
    target = models.CharField(max_length=1023)

    class Meta:
        unique_together = [('site', 'path')]


class BlogPost(models.Model):
    site = models.ForeignKey(Site)
    path = models.CharField(**PATH_FIELD_PARAMS)
    date = models.DateField()
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    public_from = models.DateTimeField(null=True, blank=True)
    visible_from = models.DateTimeField(null=True, blank=True)

    title = models.CharField(max_length=1023)
    body = models.TextField()

    def _make_path(self):
        return reverse('content_blog_post_view', kwargs=dict(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            slug=self.slug,
        ))

    def save(self, *args, **kwargs):
        if self.date and self.slug:
            self.path = self._make_path()

        return super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        unique_together = [('site', 'path'), ('site', 'date', 'slug')]
