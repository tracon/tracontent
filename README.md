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

For the client app to see the `crowd.token_key` cookie, it needs to be in the `tracon.fi` domain.

You can get around this by putting something like this in the `/etc/hosts` file (that is, `C:\Windows\System32\Drivers\etc\hosts`) **of the computer that runs your web browser**:

    127.0.0.1 localhost ssoexample-dev.tracon.fi

For your development pleasure, `kompassidev.tracon.fi` deals out cookies that do not have the "secure" flag set so that you don't need to access your development instance via HTTPS.

### Create an application in Crowd

1. Log in to the Crowd console as an admin user.
2. Navigate to Applications > Add Application.
3. On the Details tab, set Application type to Generic application, pick an application name (eg. `ssoexample`) and enter it in the Name field, and pick a password and enter it twice.
4. On the Connection tab, enter anything that looks like a URL in the URL field, and enter the Internet-facing IP address of your installation in the IP address field.
5. On the Directories tab, select the correct directories. In Tracon, this would be `Tracon ry IPA`.
6. On the Authorisation tab, either allow all users to authenticate or select some groups whose users will be allowed in.
7. Review the details on the Confirmation tab and hit Add Application.
8. Fill in the authentication details into `settings.py`:


    KOMPASSI_CROWD_URL = 'https://crowd.tracon.fi/crowd'
    KOMPASSI_CROWD_APPLICATION_NAME = 'the application name you selected in phase 3'
    KOMPASSI_CROWD_APPLICATION_PASSWORD = 'the password you selected in phase 3'

### Create an API user in Kompassi

We are lazy and will use a local Django user instead of an IPA user. If we are really lazy, we might even use the same username and password as we did for Crowd.

1. Log in to your Kompassi instance as an admin user.
2. Go to the Django admin interface at `/admin/`.
3. Navigate to Auth > Users and select Add user.
4. Pick a username and password for the API user and select `Save and continue editing`.
5. Figure out the application user group for your Kompassi installation and add the newly created user into that group.
  * In Tracon Kompassi development, this would be `turskadev-apps`.
  * In Tracon Kompassi production, this would be `turska-apps`.
6. Remember to save the modifications to the user account.
7. Fill in the authentication details into `settings.py`:


    KOMPASSI_API_URL = 'https://kompassidev.tracon.fi/api/v1'
    KOMPASSI_API_APPLICATION_NAME = 'the username you selected in phase 4'
    KOMPASSI_API_APPLICATION_PASSWORD = 'the password you selected in phase 4'

### Validation factors

Crowd requires that you use the same validation factors for refreshing the session as you did for setting the session up. The validation factors used in our installation are as follows:

* `remote_address`: Always `127.0.0.1`.
* `X-Forwarded-For`: The public, Internet-facing IP address of the browser.

In `settings.py` there are lambdas that are used to extract this information from the request object. What the lambdas should do depends on your setup:

#### Production installation behind a reverse proxy

It is recommended to install Django apps behind an Apache or nginx proxy. In this case, `REMOTE_ADDR` is always `127.0.0.1` and the real IP address is in the `X-Forwarded-For` HTTP header.

    KOMPASSI_CROWD_VALIDATION_FACTORS = {
        'remote_address': lambda request: '127.0.0.1',
        'X-Forwarded-For': lambda request: request.META['HTTP_X_FORWARDED_FOR'],
    }

#### Production or development installation without a proxy

If the Django instance is not behind a proxy and sees your public, Internet-facing IP address in `REMOTE_ADDR`, you should fake being behind a proxy as our Crowd, Confluence etc. installations **are** behind a proxy.

    KOMPASSI_CROWD_VALIDATION_FACTORS = {
        'remote_address': lambda request: '127.0.0.1',
        'X-Forwarded-For': lambda request: request.META['REMOTE_ADDR'],
    }

NB. The Django development server is not suitable for use in production, but you might use `gunicorn` or `uwsgi`.

#### Development server in a private IP address or localhost

If your development server does not get your Internet-facing IP address in either X-Forwarded-For or REMOTE_ADDR, you need to fake it in the validation factors. This is usually the case for local development setups where you have the Django instance running in either `localhost` or a (virtual) machine behind a NAT.

    KOMPASSI_CROWD_VALIDATION_FACTORS = {
        'remote_address': lambda request: '127.0.0.1',
        'X-Forwarded-For': lambda request: '84.248.69.106', # the Internet-facing IP address of your browser
    }
