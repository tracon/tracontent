# Example for interim Kompassi OAuth2 SSO

The `kompassi_oauth2` directory contains reusable code for your Django application.

## Configuration

Assuming you have an nginx proxy, this is what you would need in `settings.py`. Validation factors need to match those Crowd sees.

TODO

## Development gotchas

### "OAuth2 MUST use HTTPS"

Technically it's horribly wrong to use OAuth2 over insecure HTTP. However, it's tedious to set up TLS for development. That's why we monkey patch `oauthlib.oauth2:is_secure_transport` on `DEBUG = True`. See `kompassi_oauth2_example/settings.py`.

### Applications on `localhost` in different hosts share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this example `localhost:8001`
3. Try to log in

Expected results: You are logged in

Actual results: 500 Internal Server Error due to session not having `oauth_state` in `/oauth2/callback`

Explanation: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

Workaround: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://ssoexample.dev:8001` instead.

    127.0.0.1 localhost kompassi.dev ssoexample.dev
