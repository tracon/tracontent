from django.contrib.auth.models import User
from django.conf import settings


def user_defaults_from_kompassi(kompassi_user):
    return dict((django_key, kompassi_user[kompassi_key]) for (django_key, kompassi_key) in [
        ('username', 'username'),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'surname'),
    ])


class KompassiOAuth2AuthenticationBackend(object):
    def authenticate(self, oauth2_session=None, **kwargs):
        if oauth2_session is None:
            # Not ours (password login)
            return None

        response = oauth2_session.get(settings.KOMPASSI_API_V2_USER_INFO_URL)
        response.raise_for_status()
        kompassi_user = response.json()

        user, created = User.objects.get_or_create(
            username=kompassi_user['username'],
            defaults=user_defaults_from_kompassi(kompassi_user)
        )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesDotExist:
            return None
