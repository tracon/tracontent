# encoding: utf-8

from django.db import models


class Organizer(models.Model):
    image_file = models.FileField(
        upload_to='organizers',
        verbose_name=u'Naamakuva',
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=127,
        verbose_name=u'Etunimi',
    )

    last_name = models.CharField(
        max_length=127,
        verbose_name=u'Sukunimi',
        blank=True,
    )

    nick = models.CharField(
        max_length=127,
        verbose_name=u'Nick',
        blank=True,
    )

    job_title = models.CharField(
        max_length=127,
        verbose_name=u'Tehtävä',
        blank=True,
    )

    email = models.EmailField(
        verbose_name=u'Sähköpostiosoite',
        blank=True,
    )

    order = models.IntegerField(
        verbose_name=u'Järjestys',
        help_text=u'Pienin ensin, samannumeroiset sukunimen mukaan',
        default=0,
    )

    class Meta:
        verbose_name = u'Järjestäjä'
        verbose_name_plural = u'Järjestäjät'
        ordering = ('order', 'last_name', 'first_name')

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        if self.nick:
            return u'{first_name} ”{nick}” {last_name}'.format(
                first_name=self.first_name,
                nick=self.nick,
                last_name=self.last_name,
            )
        else:
            return u'{first_name} {last_name}'.format(
                first_name=self.first_name,
                last_name=self.last_name,
            )