# -*- coding: utf-8 -*-
import os
# for relative paths
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Custom data directory
DATA_ROOT = here('data')

ADMINS = (
    ('Pierre Romera', 'hello@pirhoo.com')
)

DEFAULT_FROM_EMAIL = 'Detective.io <contact@detective.io>'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db'
    }
}

NEO4J_DATABASES = {
    'default' : {
        'HOST': "127.0.0.1",
        'PORT': 7474,
        'ENDPOINT':'/db/data'
    }
}

DATABASE_ROUTERS        = ['neo4django.utils.Neo4djangoIntegrationRouter']
SESSION_ENGINE          = "django.contrib.sessions.backends.db"
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/public/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = here('staticfiles')

LOGIN_URL = "/admin"
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Bower components
    ('components', here('static/components') ),
    here("detective/static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY', '#_o0^tt=lv1k8k-h=n%^=e&amp;vnvcxpnl=6+%&amp;+%(2!qiu!vtd9%')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'app.middleware.crossdomainxhr.XsSharing',
    # add urlmiddleware after all other middleware.
    'urlmiddleware.URLMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'app.wsgi.application'

TEMPLATE_DIRS = (
    here('detective/templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# JS/CSS COMPRESSOR SETTINGS
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio --bare'),
    ('text/less', 'lessc --include-path="%s" {infile} {outfile}' % here('static') ),
)

# Activate CSS minifier
COMPRESS_CSS_FILTERS = (
    "app.detective.compress_filter.CustomCssAbsoluteFilter",
    "compressor.filters.template.TemplateFilter",
)

COMPRESS_JS_FILTERS = (
    "compressor.filters.template.TemplateFilter",
)

COMPRESS_TEMPLATE_FILTER_CONTEXT = {
    'STATIC_URL': STATIC_URL
}

COMPRESS_ENABLED = False
#INTERNAL_IPS = ('127.0.0.1',)

TASTYPIE_DEFAULT_FORMATS = ['json']

INSTALLED_APPS = (
    'neo4django.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    # Sign up activation
    'registration',
    # Compresses linked and inline JavaScript or CSS into a single cached file.
    'compressor',
    # API generator
    'tastypie',
    # Email backend
    "djrill",
    'password_reset',
    # Manage migrations
    'south',
    # Rich text editor
    'tinymce',
    # Internal
    'app.detective',
    'app.detective.permissions',
)

# Add customs app to INSTALLED_APPS
from app.detective.utils import get_topics_modules
INSTALLED_APPS = INSTALLED_APPS + get_topics_modules()

MANDRILL_API_KEY = os.getenv("MANDRILL_APIKEY")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
# One-week activation window
ACCOUNT_ACTIVATION_DAYS = 7

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
