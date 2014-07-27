# Example for interim Kompassi SSO via Crowd

The `kompassi_crowd` directory contains reusable code for your Django application. Would package it and release it into PyPI if this wasn't just a hacky interim solution.

## Configuration

Assuming you have an nginx proxy, this is what you would need in `settings.py`. Validation factors need to match those Crowd sees.

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        # Has to be after AuthenticationMiddleware
        'kompassi_crowd.middleware.KompassiCrowdAuthenticationMiddleware',

        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    AUTHENTICATION_BACKENDS = (
        # Has to be before ModelBackend
        'kompassi_crowd.backends.KompassiCrowdAuthenticationBackend',

        'django.contrib.auth.backends.ModelBackend',
    )

    KOMPASSI_CROWD_URL = 'https://crowd.tracon.fi/crowd'
    KOMPASSI_CROWD_APPLICATION_NAME = 'ssoexample'
    KOMPASSI_CROWD_APPLICATION_PASSWORD = 'fill me in'
    KOMPASSI_CROWD_SESSION_URL = '{KOMPASSI_CROWD_URL}/rest/usermanagement/1/session'.format(**locals())
    KOMPASSI_CROWD_COOKIE_NAME = 'crowd.token_key'
    KOMPASSI_CROWD_VALIDATION_FACTORS = {
        'remote_address': lambda request: '127.0.0.1',
        'X-Forwarded-For': lambda request: request.META['HTTP_X_FORWARDED_FOR'],
    }
    KOMPASSI_API_URL = 'https://kompassidev.tracon.fi/api/v1'
    KOMPASSI_API_APPLICATION_NAME = KOMPASSI_CROWD_APPLICATION_NAME
    KOMPASSI_API_APPLICATION_PASSWORD = KOMPASSI_CROWD_APPLICATION_PASSWORD

    LOGIN_URL = 'https://kompassidev.tracon.fi/crowd'
    LOGOUT_URL = 'https://kompassidev.tracon.fi/logout'


## Development gotchas

This is one tricky S.O.B. to develop due to multiple security measures.

### Cookie domain

For the client app to see the `crowd.token_key` cookie, it needs to be in the `tracon.fi` domain. You can get around this by putting something like this in `/etc/hosts` (that is, `C:\Windows\System32\Drivers\etc\hosts`):

    127.0.0.1 localhost ssoexample-dev.tracon.fi

For your development pleasure, `kompassidev.tracon.fi` deals out cookies that do not have the "secure" flag set.

### Application password and IP

For obvious reasons, I will not put a working application password in a public example.

You need to create an application user in two places:

* in the Kompassi instance you are using for authentication (put it in the `{slug}-apps` group)
* in Crowd (remember to allow the public IP of your workstation in the Crowd config for your application)

### Validation factors

You probably don't have a reverse proxy in your development setup, so you need to fake the validation factors.

    KOMPASSI_CROWD_VALIDATION_FACTORS = {
        'remote_address': lambda request: '127.0.0.1',
        'X-Forwarded-For': lambda request: '84.248.69.106', # your Internet-facing IP address
    }
