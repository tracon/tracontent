# Content management system for Tracon 2016 and forwards

Too long we have suffered of Wordpress, Drupal and PencilBlue. We shall have content! And we shall be content!

## Getting started

First, make sure `kompassi.dev` and `tracontent.dev` resolve to localhost via `/etc/hosts`:

    127.0.0.1 localhost kompassi.dev tracontent.dev

Next, install and run development instance of [Kompassi](/tracon/kompassi) if you don't yet have one:

    virtualenv venv-kompassi
    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -r requirements.txt
    ./manage.py setup --test
    ./manage.py runserver 127.0.0.1:8000
    iexplore http://kompassi.dev:8000

`./manage.py setup --test` created a test user account `mahti` with password `mahti` in your Kompassi development instance.

Now, in another terminal, install and run this example:

    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi-oauth2-example.git
    cd kompassi-oauth2-example
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://tracontent.dev:8001

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

## Kompassi OAuth2 Enabled

For more information, see the [Kompassi OAuth2 Example](/tracon/kompassi-oauth2-example).

## License

    The MIT License (MIT)

    Copyright (c) 2014–2015 Santtu Pajukanta

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
