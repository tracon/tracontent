# TraContent CMS

Too long have we suffered of Wordpress, Drupal and PencilBlue. We shall have content! And we shall be content!

## Standard Edition vs. Enterprise Edition

Here's a cool feature matrix:

| Feature | Standard Edition | Enterprise Edition |
|---------|------------------|--------------------|
| License | MIT | MIT |
| Price | Free | Free |
| Support | Purchased separately | Purchased separately |
| Multisite support | Yes (always on) | Yes (always on) |
| OAuth2 authentication | No | Yes |

### No, really, what's the difference?

If you have Kompassi OAuth2 support enabled, you're running the Enterprise Edition. Because starships, that's why :)

## Getting started

Docker required. I will not give you support for development without Docker.

    docker-compose up

This will set up a PostgreSQL database and the Tracontent backend in containers. It will also automatically run `python manage.py setup` in the backend container to set up the site with some placeholder pages.

You should now be able to view the site at [http://localhost:8001](http://localhost:8001).

Note that the login links probably try to log you in via OAuth2 which will fail. Use [http://localhost:8001/admin/login/](http://localhost:8001/admin/login/) instead.

## Kompassi OAuth2 Enabled

For more information, see the [Kompassi OAuth2 Example](/tracon/kompassi-oauth2-example).

## License

    The MIT License (MIT)

    Copyright (c) 2014–2018 Santtu Pajukanta
    Copyright © 2015 Aarni Koskela

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

The work of Santtu Pajukanta on Kompassi has been partially sponsored by [Leonidas Oy](https://leonidasoy.fi/opensource).
