import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '9()(lzm)jdr$szjfdx8^^#j_6efj@d&$9pb6l2h&=udxom3(bn'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['ssoexample.tracon.fi']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'example',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'kompassi_crowd.middleware.KompassiCrowdAuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'kompassi_crowd.backends.KompassiCrowdAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'kompassi_crowd_sso_example.urls'

WSGI_APPLICATION = 'kompassi_crowd_sso_example.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'kompassi_crowd_sso_example.sqlite3'),
    }
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
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'kompassi_crowd': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
    }
}

LANGUAGE_CODE = 'fi-fi'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

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
