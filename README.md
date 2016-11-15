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

Python 3.5 required. Python 2.7 might work, but is no longer supported.

### Docker

TBD.

### Linux, OS X

Install C dependencies:

    sudo apt-get install python-dev libz-dev libjpeg-dev libffi-dev libssl-dev build-essential

Install Python dependencies:

    virtualenv venv-tracontent
    source venv-tracontent/bin/activate
    git clone https://github.com/tracon/tracontent.git
    cd tracontent
    pip install -r requirements.txt
    
The `DEBUG` environment variable is required to run the default development configuration:

    export DEBUG=1
    
### Windows

PowerShell recommended for running commands. Make sure you have `pip` installed and update `setuptools` and `wheel`:

    easy_install-3.5.exe pip
    pip install -U setuptools wheel virtualenv

Install Python dependencies:

    set-executionpolicy -scope CurrentUser RemoteSigned
    python -m venv venv-tracontent
    venv-tracontent\Scripts\activate.ps1
    git clone https://github.com/tracon/tracontent.git
    cd tracontent
    pip install -r requirements.txt

The `DEBUG` environment variable is required to run the default development configuration:

    $env:DEBUG = 1

### Common

Setup basic example content:

    python manage.py setup
    python manage.py setup_tracon11 127.0.0.1:8001

Run the server and view the site in your favourite web browser:

    python manage.py runserver 127.0.0.1:8001
    iexplore http://127.0.0.1:8001
    iexplore http://127.0.0.1:8001/admin/login/

Note that due to multisite support, `127.0.0.1:8001` needs to match whatever `host:port` you use to access your development instance.

The `python manage.py setup` command created a superuser called `mahti` with the password `mahti`.

## Kompassi OAuth2 Enabled

For more information, see the [Kompassi OAuth2 Example](/tracon/kompassi-oauth2-example).

## License

    The MIT License (MIT)

    Copyright (c) 2014–2016 Santtu Pajukanta

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
