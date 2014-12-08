#coding: utf-8
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'wwgwj3gc7al-mwofc6u0xjvi4&@7d&^59mvb=nien887rqjwpb'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_select2',

    'base',
    'hockeyapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sportomatics.urls'
WSGI_APPLICATION = 'sportomatics.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'ru'
LANGUAGES = (('ru','Russian'),)
TIME_ZONE = 'UTC'
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
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

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
    'MENU_EXCLUDE': ('sites',),
}


try:
    from local_settings import *
except ImportError:
    pass