# encoding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracontent.settings")

from django.core.wsgi import get_wsgi_application

from dj_static import MediaCling


application = MediaCling(get_wsgi_application())
