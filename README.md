# Example for Kompassi OAuth2 SSO

This is an example of OAuth2 authentication against the [Kompassi](/tracon/kompassi) event management system. The `kompassi_oauth2` directory contains reusable code for your Django application.

## Getting started

First, make sure `kompassi.dev` and `ssoexample.dev` resolve to localhost via `/etc/hosts`:

    127.0.0.1 localhost kompassi.dev ssoexample.dev

Next, install and run development instance of [Kompassi](/tracon/kompassi) if you don't yet have one:

    virtualenv venv-kompassi
    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -r requirements.txt
    ./manage.py setup --test # will create an user called "mahti" with password "mahti"
    ./manage.py runserver 127.0.0.1:8000
    iexplore http://kompassi.dev:8000

Now, in another terminal, install and run this example:

    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi-oauth2-example.git
    cd kompassi-oauth2-example
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser # use something else than "mahti" for username
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://ssoexample.dev:8001

When you click the "Go to protected page" link, you should be transferred to your Kompassi development instance. Log in with user `mahti` and password `mahti`, authorize the example application to receive your user info, and you should see the protected page.

## Configuration

```python
AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

KOMPASSI_OAUTH2_AUTHORIZATION_URL = 'http://kompassi.dev:8000/oauth2/authorize'
KOMPASSI_OAUTH2_TOKEN_URL = 'http://kompassi.dev:8000/oauth2/token'
KOMPASSI_OAUTH2_CLIENT_ID = 'kompassi_insecure_test_client_id'
KOMPASSI_OAUTH2_CLIENT_SECRET = 'kompassi_insecure_test_client_secret'
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = 'http://kompassi.dev:8000/api/v2/people/me'
```

## Development gotchas

### "OAuth2 MUST use HTTPS"

Technically it's horribly wrong to use OAuth2 over insecure HTTP. However, it's tedious to set up TLS for development. That's why we monkey patch `oauthlib.oauth2:is_secure_transport` on `DEBUG = True`. See `kompassi_oauth2_example/settings.py`.

### Applications on `localhost` in different ports share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this example `localhost:8001`
3. Try to log in

Expected results: You are logged in

Actual results: 500 Internal Server Error due to session not having `oauth_state` in `/oauth2/callback`

Explanation: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

Workaround: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://ssoexample.dev:8001` instead.

    127.0.0.1 localhost kompassi.dev ssoexample.dev
