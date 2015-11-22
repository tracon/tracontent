# encoding: utf-8

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models


NAME_DISPLAY_STYLE_FORMATS = dict(
    firstname=u'{self.first_name}',
    firstname_nick_surname=u'{self.first_name} "{self.nick}" {self.surname}',
    firstname_surname=u'{self.first_name} {self.surname}',
    nick=u'{self.nick}',
)
NAME_DISPLAY_STYLE_CHOICES = [
    (u'firstname_nick_surname', u'Etunimi "Nick" Sukunimi'),
    (u'firstname_surname', u'Etunimi Sukunimi'),
    (u'firstname', u'Etunimi'),
    (u'nick', u'Nick'),
]


def delegate_to_user(field_name):
    @property
    def _the_property(self):
        return getattr(self.user, field_name)

    return _the_property


class UserMetaMethodsMixin(object):
    first_name = delegate_to_user('first_name')
    surname = delegate_to_user('last_name')

    @property
    def name_display_style(self):
        if self.preferred_name_display_style:
            return self.preferred_name_display_style
        else:
            if self.nick:
                return 'firstname_nick_surname'
            else:
                return 'firstname_surname'

    def get_full_name(self):
        return NAME_DISPLAY_STYLE_FORMATS[self.name_display_style].format(self=self).strip()

    def get_short_name(self):
        if self.nick and 'nick' in self.name_display_style:
            return self.nick.strip()
        else:
            return self.first_name.strip() if self.first_name else u''

    @classmethod
    def get_for_user(cls, user):
        if user.is_anonymous():
            return ANONYMOUS_USER_META
        else:
            user_meta, created = cls.objects.get_or_create(user=user)
            return user_meta


class UserMeta(models.Model, UserMetaMethodsMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'Käyttäjä')
    nick = models.CharField(blank=True, max_length=1023, help_text=u'Lempi- tai kutsumanimi')

    preferred_name_display_style = models.CharField(
        max_length=31,
        verbose_name=u'Nimen esittäminen',
        help_text=u'Tässä voit vaikuttaa siihen, missä muodossa nimesi esitetään (esim. painetaan badgeesi).',
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = u'Käyttäjän lisätiedot'
        verbose_name_plural = u'Käyttäjien lisätiedot'


class AnonymousUserMeta(UserMetaMethodsMixin):
    def __init__(self):
        self.user = AnonymousUser()
        self.nick = u'Anonymous User'
        self.preferred_name_display_style = u'nick'


ANONYMOUS_USER_META = AnonymousUserMeta()
