from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models


NAME_DISPLAY_STYLE_FORMATS = dict(
    firstname='{self.first_name}',
    firstname_nick_surname='{self.first_name} "{self.nick}" {self.surname}',
    firstname_surname='{self.first_name} {self.surname}',
    nick='{self.nick}',
)
NAME_DISPLAY_STYLE_CHOICES = [
    ('firstname_nick_surname', 'Etunimi "Nick" Sukunimi'),
    ('firstname_surname', 'Etunimi Sukunimi'),
    ('firstname', 'Etunimi'),
    ('nick', 'Nick'),
]


def delegate_to_user(field_name):
    @property
    def _the_property(self):
        return getattr(self.user, field_name)

    return _the_property


class UserMetaMethodsMixin:
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
            return self.first_name.strip() if self.first_name else ''

    @classmethod
    def get_for_user(cls, user):
        if user.is_anonymous:
            return ANONYMOUS_USER_META
        else:
            user_meta, created = cls.objects.get_or_create(user=user)
            return user_meta


class UserMeta(models.Model, UserMetaMethodsMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Käyttäjä', on_delete=models.CASCADE)
    nick = models.CharField(blank=True, max_length=1023, help_text='Lempi- tai kutsumanimi')

    preferred_name_display_style = models.CharField(
        max_length=31,
        verbose_name='Nimen esittäminen',
        help_text='Tässä voit vaikuttaa siihen, missä muodossa nimesi esitetään (esim. painetaan badgeesi).',
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Käyttäjän lisätiedot'
        verbose_name_plural = 'Käyttäjien lisätiedot'


class AnonymousUserMeta(UserMetaMethodsMixin):
    def __init__(self):
        self.user = AnonymousUser()
        self.nick = 'Anonymous User'
        self.preferred_name_display_style = 'nick'


ANONYMOUS_USER_META = AnonymousUserMeta()
