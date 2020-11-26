import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracontent.settings")

from django.core.wsgi import get_wsgi_application

from dj_static import MediaCling
from django.urls import path, re_path


application = MediaCling(get_wsgi_application())
