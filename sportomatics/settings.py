#coding: utf-8
import os
import time

from django.utils.translation import ugettext_lazy as _

from celery import local_celery_crontab


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'wwgwj3gc7al-mwofc6u0xjvi4&@7d&^59mvb=nien887rqjwpb'

SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
                    '141.8.196.179:443',
                    '94.23.21.186',
                    '.sportomatics.ru',
                    'localhost',
]

INSTALLED_APPS = (
    'suit',
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'daterange_filter',
    'django_select2',
    'filer',
    'easy_thumbnails',
    'registration',
    'relatives',
    'rest_framework',
    'rosetta',
    'social_auth',

    'accounts',
    'addresses',
    'api',
    'base',
    'bower',
    'hockeyapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.browserid.BrowserIDBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.disqus.DisqusBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    # 'social_auth.backends.contrib.live.LiveBackend',
    # 'social_auth.backends.contrib.skyrock.SkyrockBackend',
    # 'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    # 'social_auth.backends.contrib.readability.ReadabilityBackend',
    # 'social_auth.backends.contrib.fedora.FedoraBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
LINKEDIN_CONSUMER_KEY = ''
LINKEDIN_CONSUMER_SECRET = ''
ORKUT_CONSUMER_KEY = ''
ORKUT_CONSUMER_SECRET = ''
GOOGLE_CONSUMER_KEY = ''
GOOGLE_CONSUMER_SECRET = ''
GOOGLE_OAUTH2_CLIENT_ID = '110426058524-3bdf21qirbucr548e8l5jg5mkdcupa2p.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'RAqyLD7ZY1gVkEqndwYRv-rJ'
FOURSQUARE_CONSUMER_KEY = ''
FOURSQUARE_CONSUMER_SECRET = ''
VK_APP_ID = ''
VK_API_SECRET = ''
LIVE_CLIENT_ID = ''
LIVE_CLIENT_SECRET = ''
SKYROCK_CONSUMER_KEY = ''
SKYROCK_CONSUMER_SECRET = ''
YAHOO_CONSUMER_KEY = ''
YAHOO_CONSUMER_SECRET = ''
READABILITY_CONSUMER_SECRET = ''
READABILITY_CONSUMER_SECRET = ''

ROOT_URLCONF = 'sportomatics.urls'
WSGI_APPLICATION = 'sportomatics.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'ru'
LANGUAGES = (   ('ru',_('Russian')),
                ('en', _('English')),
            )
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

CELERY_ACCEPT_CONTENT = ('pickle', 'json', 'msgpack', 'yaml')
BROKER_URL = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'hockeyapp-periodic-update-clubs-every-monday-midnight': {
        'task': 'hockeyapp.tasks.periodic_update_clubs',
        'schedule': local_celery_crontab(hour=1, minute=30, day_of_week=1),
    },
    'hockeyapp-periodic-update-schedules-every-day-midnight': {
        'task': 'hockeyapp.tasks.periodic_update_schedules',
        'schedule': local_celery_crontab(hour=1, minute=30),
    },
    'hockeyapp-periodic-get-matches-every-day-midnight': {
        'task': 'hockeyapp.tasks.periodic_get_matches',
        'schedule': local_celery_crontab(hour=2, minute=10),
    },
    #'hockeyapp-periodic_get-clubs-instagram_pictures-every-day-midnight': {
        #'task': 'hockeyapp.tasks.get_clubs_instagram_pictures',
        #'schedule': local_celery_crontab(hour=0, minute=0),
    #},
    'hockeyapp-periodic-player-generate-timeline': {
        'task': 'hockeyapp.tasks.periodic_player_generate_timeline',
        'schedule': local_celery_crontab(hour=3, minute=0),
    },
    'hockeyapp-periodic-player-recalc-counters': {
        'task': 'hockeyapp.tasks.periodic_player_recalc_counters',
        'schedule': local_celery_crontab(hour=5, minute=0),
    },
}
CELERY_IGNORE_RESULT = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
FILER_PAGINATE_BY = 50

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "_static"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
             '--no-start-message',
             '--verbosity=2',
             '--with-fixture-bundling',
            ]

SUIT_CONFIG = {
    'ADMIN_NAME': 'Sportomatics',
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU': (
        {'app': 'accounts',},
        {'app': 'addresses',},
        {'app': 'base',},
        {'app': 'filer',},
        {'app': 'hockeyapp',},
        {
            'label': _('Club leagues add form'), 
            'icon':'icon-edit', 
            'url': '/admin/hockeyapp/leagueclub_multi_add/'
        },
        {'label': _('Translation'), 'icon':'icon-globe', 'url': '/rosetta/pick/'},
    ),
    'MENU_EXCLUDE': ('sites', 'auth'),
    'LIST_PER_PAGE': 50,
}

#parser
LAST_PROTOCAL_GAME = 44123

#session
SESSION_ENGINE = 'redis_sessions.session'

#registration
ACCOUNT_ACTIVATION_DAYS = 7
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no-reply@sportomatics.ru'

#rosetta
ROSETTA_MESSAGES_PER_PAGE = 100
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_UWSGI_AUTO_RELOAD = True
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'ru'
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = 'Russian'
ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

#social
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

#instagram api
INSTAGRAM_ID = '0e374970926c4d459048dba13494ae2f'
INSTAGRAM_SECRET = 'effcd0e38f154c28931c7f3655260472'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:0",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

MIGRATION_MODULES = {
    'filer': 'filer.migrations_django',
}

# project frontend's version
PROJECT_VERSION = int(time.time())

try:
    from local_settings import *
except ImportError:
    pass

