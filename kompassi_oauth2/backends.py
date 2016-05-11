from django.contrib.auth.models import User, Group
from django.conf import settings

from users.models import UserMeta


STAFF_GROUPS = set(settings.KOMPASSI_EDITOR_GROUPS)
STAFF_GROUPS.add(settings.KOMPASSI_ADMIN_GROUP)


def user_attrs_from_kompassi(kompassi_user):
    return dict((django_key, accessor_func(kompassi_user)) for (django_key, accessor_func) in [
        ('username', lambda u: u['username']),
        ('email', lambda u: u['email']),
        ('first_name', lambda u: u['first_name']),
        ('last_name', lambda u: u['surname']),
        ('is_superuser', lambda u: settings.KOMPASSI_ADMIN_GROUP in u['groups']),
        ('is_staff', lambda u: bool(STAFF_GROUPS.intersection(kompassi_user['groups'])),
        ('groups', lambda u: [Group.objects.get_or_create(name=group_name)[0] for group_name in u['groups']]),
    ])


def user_meta_attrs_from_kompassi(kompassi_user):
    return dict((django_key, accessor_func(kompassi_user)) for (django_key, accessor_func) in [
        ('nick', lambda u: u['nick']),
        ('preferred_name_display_style', lambda u: u['preferred_name_display_style']),
    ])


class KompassiOAuth2AuthenticationBackend(object):
    def authenticate(self, oauth2_session=None, **kwargs):
        if oauth2_session is None:
            # Not ours (password login)
            return None

        response = oauth2_session.get(settings.KOMPASSI_API_V2_USER_INFO_URL)
        response.raise_for_status()
        kompassi_user = response.json()

        # Non-editor users may not log in via OAuth2
        if not STAFF_GROUPS.intersection(kompassi_user['groups']):
            return None

        user, created = User.objects.get_or_create(username=kompassi_user['username'])
        for key, value in user_attrs_from_kompassi(kompassi_user).items():
            setattr(user, key, value)
        user.save()

        user_meta = UserMeta.get_for_user(user)
        for key, value  in user_meta_attrs_from_kompassi(kompassi_user).items():
            setattr(user_meta, key, value)
        user_meta.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesDotExist:
            return None
