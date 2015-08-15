# encoding: utf-8

from collections import namedtuple

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now

from .utils import slugify


validate_slug = RegexValidator(
    regex=r'[a-z0-9-]+',
    message=u'Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.'
)

validate_path = RegexValidator(
    regex=r'[a-z0-9-/]+',
    message=u'Polku saa sisältää vain pieniä kirjaimia, numeroita, väliviivoja sekä kauttaviivoja.'
)


class CommonFields:
    path = dict(
        max_length=1023,
        validators=[validate_path],
        verbose_name=u'Polku',
        help_text=u'Polku määritetään automaattisesti teknisen nimen perusteella.',
    )

    slug = dict(
        blank=True, # actually not, but autogenerated anyway
        max_length=63,
        validators=[validate_slug],
        verbose_name=u'Tekninen nimi',
        help_text=u'Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
            u'merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Jos jätät teknisen nimen tyhjäksi, '
            u'se generoidaan automaattisesti otsikosta.'
    )

    title = dict(
        max_length=1023,
        verbose_name=u'Otsikko',
        help_text=u'Otsikko näytetään automaattisesti sivun ylälaidassa sekä valikossa. Älä lisää erillistä pääotsikkoa sivun tekstiin.',
    )

    body = dict(
        blank=True,
        verbose_name=u'Leipäteksti',
    )

    template = dict(
        max_length=127,
        verbose_name=u'Sivupohja',
        help_text=u'Sivut näytetään käyttäen tätä sivupohjaa. Tämännimisen sivupohjan tulee löytyä lähdekoodista.',
    )

    site = dict(
        verbose_name=u'Sivusto',
        help_text=u'Sivusto, jolle tämä sivu kuuluu. HUOM! Kun haluat luoda saman sivun toiselle sivustolle, älä siirrä vanhaa sivua vaan käytä sivunkopiointitoimintoa.',
    )

    public_from = dict(
        null=True,
        blank=True,
        verbose_name=u'Julkaisuaika',
        help_text=u'Sivu on tästä hetkestä alkaen myös sisäänkirjautumattomien käyttäjien luettavissa, jos nämä tietävät osoitteen. Jätä tyhjäksi, jos haluat jättää sivun luonnokseksi.',
    )

    visible_from = dict(
        null=True,
        blank=True,
        verbose_name=u'Näkyvissä alkaen',
        help_text=u'Sivu on tästä hetkestä alkaen näkyvissä valikossa tai listauksessa. Jätä tyhjäksi, jos haluat jättää sivun piilotetuksi.',
    )


class SiteSettings(models.Model):
    site = models.OneToOneField(Site)
    title = models.CharField(
        max_length=1023,
        verbose_name=u'Sivuston otsikko',
        help_text=u'Sivuston otsikko näkyy mm. selaimen välilehden otsikossa.',
    )
    base_template = models.CharField(**CommonFields.template)

    @classmethod
    def get_or_create_dummy(cls):
        site, unused = Site.objects.get_or_create(domain='example.com')

        return cls.objects.get_or_create(
            site=site,
            defaults=dict(
                title='Test site',
                base_template='example_base.jade',
            )
        )

    def get_menu(self, t=None, current_url=None):
        if t is None:
            t = now()

        return [
            page.get_menu_entry(t=t, current_url=current_url)
            for page in Page.objects.filter(site=self.site, parent=None, visible_from__lte=t).prefetch_related('child_page_set').all()
        ]

    class Meta:
        verbose_name = u'sivuston asetukset'
        verbose_name = u'sivustojen asetukset'


BaseMenuEntry = namedtuple('MenuEntry', 'active href text children')
class MenuEntry(BaseMenuEntry):
    @property
    def active_css(self):
        return 'active' if self.active else ''


class Page(models.Model):
    site = models.ForeignKey(Site, **CommonFields.site)
    path = models.CharField(**CommonFields.path)
    parent = models.ForeignKey('Page',
        null=True,
        blank=True,
        verbose_name=u'Yläsivu',
        help_text=u'Jos valitset tähän sivun, tämä sivu luodaan valitun sivun alaisuuteen. Jos jätät tämän tyhjäksi, sivu luodaan päätasolle.',
        related_name='child_page_set',
    )

    slug = models.CharField(**CommonFields.slug)

    public_from = models.DateTimeField(**CommonFields.public_from)
    visible_from = models.DateTimeField(**CommonFields.visible_from)

    title = models.CharField(**CommonFields.title)
    override_menu_text = models.CharField(
        max_length=1023,
        blank=True,
        verbose_name=u'Valikkoteksti',
        help_text=u'Sivu näkyy tällä nimellä valikossa. Jos jätät tämän tyhjäksi, käytetään otsikkoa.',
    )
    order = models.IntegerField(
        default=0,
        verbose_name=u'Järjestys',
        help_text=u'Saman yläsivun alaiset sivut järjestetään valikossa tämän luvun mukaan nousevaan '
            u'järjestykseen (pienin ensin).'
    )
    body = models.TextField(**CommonFields.body)

    @property
    def edit_link(self):
        return reverse('admin:content_page_change', args=(self.id,))

    @property
    def menu_text(self):
        if self.override_menu_text:
            return self.override_menu_text
        else:
            return self.title

    @property
    def is_front_page(self):
        return self.parent is None and self.slug == 'front-page'

    def get_absolute_url(self):
        if self.is_front_page:
            return '/'
        else:
            return '/' + self.path

    def get_menu_entry(self, child_levels=1, t=None, current_url=None):
        # Guard against infinite recursion on parent loop and prevent lots of queries on default 2-level menu structure
        if child_levels > 0:
            children = [
                child_page.get_menu_entry(
                    child_levels=child_levels - 1,
                    t=t,
                    current_url=current_url,
                )

                # TODO check if this hits the prefetch
                for child_page in self.child_page_set.filter(visible_from__lte=t)
            ]
        else:
            children = []

        href = self.get_absolute_url()

        if current_url:
            if children:
                active = current_url.startswith(href)
            else:
                active = current_url == href
        else:
            active = False

        return MenuEntry(
            active=active,
            href=href,
            text=self.menu_text,
            children=children,
        )

    def _make_path(self):
        if self.parent is None:
            return self.slug
        else:
            return self.parent.path + '/' + self.slug

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        if self.slug:
            self.path = self._make_path()

        return_value = super(Page, self).save(*args, **kwargs)

        # In case path changed, update child pages' paths.
        # TODO prevent parent loop in somewhere else
        for child_page in self.child_page_set.all():
            child_page.save()

    def __unicode__(self):
        return u'{domain}/{path}'.format(
            domain=self.site.domain if self.site is not None else None,
            path=self.path,
        )

    class Meta:
        verbose_name = u'sivu'
        verbose_name_plural = u'sivut'
        unique_together = [('site', 'path'), ('site', 'parent', 'slug')]

        # Usually searches are filtered by site and parent, so we skip them from the ordering.
        ordering = ('order',)


class Redirect(models.Model):
    site = models.ForeignKey(Site)
    path = models.CharField(**CommonFields.path)
    target = models.CharField(max_length=1023)

    class Meta:
        unique_together = [('site', 'path')]
        verbose_name = u'uudelleenohjaus'
        verbose_name_plural = u'uudelleenohjaukset'


class BlogPost(models.Model):
    site = models.ForeignKey(Site, **CommonFields.site)
    path = models.CharField(**CommonFields.path)
    date = models.DateField(
        verbose_name=u'Päivämäärä',
        help_text=u'Päivämäärä on osa postauksen osoitetta. Älä muuta päivämäärää julkaisun jälkeen.',
    )
    slug = models.CharField(**CommonFields.slug)

    public_from = models.DateTimeField(**CommonFields.public_from)
    visible_from = models.DateTimeField(**CommonFields.visible_from)

    title = models.CharField(**CommonFields.title)
    body = models.TextField(**CommonFields.body)

    @property
    def edit_link(self):
        return reverse('admin:content_blogpost_change', args=(self.id,))

    def get_absolute_url(self):
        return '/' + self.path

    def _make_path(self):
        return reverse('content_blog_post_view', kwargs=dict(
            year=self.date.year,
            month="{:02d}".format(self.date.month),
            day="{:02d}".format(self.date.day),
            slug=self.slug,
        ))[1:] # remove leading /

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        if self.date and self.slug:
            self.path = self._make_path()

        return super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'blogipostaus'
        verbose_name_plural = u'blogipostaukset'
        unique_together = [('site', 'path'), ('site', 'date', 'slug')]
