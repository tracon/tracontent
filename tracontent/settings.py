# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime, timedelta
from email.utils import parseaddr

from django.utils.translation import ugettext_lazy as _

import environ


env = environ.Env(DEBUG=(bool, False),)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def mkpath(*args):
    return os.path.abspath(os.path.join(BASE_DIR, *args))


DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY', default=('' if not DEBUG else 'xxx'))
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=('' if not DEBUG else '*')).split()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ADMINS = [parseaddr(addr) for addr in env('ADMINS', default='').split(',') if addr]

# Sending email
if env('EMAIL_HOST', default=''):
    EMAIL_HOST = env('EMAIL_HOST')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='spam@example.com')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'reversion',

    'kompassi_oauth2',
    'content',
    'ads',
    'resources',
    'users',

    'site_specific.tracommon',

    'site_specific.simple',
    'site_specific.traconx',
    'site_specific.tracon11',
    'site_specific.aicon',
    'site_specific.hitpoint2015',
    'site_specific.animecon2016',
    'site_specific.conikuvat',
    'site_specific.hitpoint2017',
    'site_specific.tracon2017',
    'site_specific.tracon2018',
    'site_specific.aicon2018',
    'site_specific.tracon2019',
    'site_specific.hitpoint2019',

    'site_specific.japsufi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [mkpath('tracontent', 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'content.context_processors.content_context',
                'users.context_processors.users_context',
            ],
            # PyPugJS part:
            'loaders': [
                ('pypugjs.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': [
                'pypugjs.ext.django.templatetags',
            ],
        },
    },
]

if 'ads' in INSTALLED_APPS:
    TEMPLATES[0]['OPTIONS']['context_processors'] += [
        'ads.context_processors.ads_context',
    ]

ROOT_URLCONF = 'tracontent.urls'

WSGI_APPLICATION = 'tracontent.wsgi.application'

DATABASES = {
    'default': env.db(default='sqlite:///tracontent.sqlite3'),
}

CACHES = {
    'default': env.cache(default='locmemcache://'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'kompassi_oauth2': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'resources': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        }
    }
}

LANGUAGE_CODE = 'fi-fi'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = mkpath('static')

MEDIA_URL = '/media/'
MEDIA_ROOT = mkpath('media')

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = '/static/common/js/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'],
            ['NumberedList', 'BulletedList', 'Indent', 'Outdent', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Image', 'Table', 'Link', 'Unlink', 'Anchor', 'SectionLink', 'Subscript', 'Superscript'],
            ['Undo', 'Redo'],
            ['Source'],
            ['Maximize']
        ],
        'extraPlugins': 'image2',
    },
}

KOMPASSI_INSTALLATION_SLUG = env('KOMPASSI_INSTALLATION_SLUG', default='turska')
KOMPASSI_HOST = env('KOMPASSI_HOST', default='https://kompassi.eu')
KOMPASSI_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_HOST}/oauth2/authorize'.format(**locals())
KOMPASSI_OAUTH2_TOKEN_URL = '{KOMPASSI_HOST}/oauth2/token'.format(**locals())
KOMPASSI_OAUTH2_CLIENT_ID = env('KOMPASSI_OAUTH2_CLIENT_ID', default='kompassi_insecure_test_client_id')
KOMPASSI_OAUTH2_CLIENT_SECRET = env('KOMPASSI_OAUTH2_CLIENT_SECRET', default='kompassi_insecure_test_client_secret')
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = '{KOMPASSI_HOST}/api/v2/people/me'.format(**locals())
KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE = '{kompassi_host}/api/v2/events/{event_slug}'
KOMPASSI_ADMIN_GROUP = env('KOMPASSI_ADMIN_GROUP', default='admins')
KOMPASSI_EDITOR_GROUPS = env('KOMPASSI_EDITOR_GROUPS', default='tracontent-staff').split()
KOMPASSI_PROGRAMME_EXPIRY_SECONDS = 300

LOGIN_URL = '/oauth2/login' if 'kompassi_oauth2' in INSTALLED_APPS else '/admin/login/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '{KOMPASSI_HOST}/logout'.format(**locals())

TRACONTENT_BLOG_AUTO_EXCERPT_MAX_CHARS = 300
TRACONTENT_BLOG_COMMENT_MODERATORS = [
    parseaddr(addr)
    for addr in env('TRACONTENT_BLOG_COMMENT_MODERATORS', default='').split(',')
    if addr
] or ADMINS

CRISPY_TEMPLATE_PACK = 'bootstrap3'
