import os
import sys
import environ
from worker import app

sys.dont_write_bytecode = True

################################
# HIGH PRIORITY LOCAL SETTINGS #
################################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_first_settings import *
except ImportError as e:
    if "local_first_settings" not in str(e):
        raise e


# set default values and casting
env = environ.Env()

# Django settings for server project.
DEBUG = True if env('DEBUG') == 'True' else False

ADMINS = (
    ('Guillaume Pellerin', 'guillaume.pellerin@ircam.fr'),
    ('Martin Desrumaux', 'martin.desrumaux@ircam.fr'),
)

MANAGERS = ADMINS

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'postgres',      # Not used with sqlite3.
        'PASSWORD': env('POSTGRES_PASSWORD'),  # Not used with sqlite3.
        'NAME': 'postgres',
        'HOST': 'db',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 5432,      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

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


# App path
APP_PATH = '/srv/app/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/srv/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/srv/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


RESULTS_ROOT = os.path.join(MEDIA_ROOT, 'results')

if not os.path.exists(RESULTS_ROOT):
    os.makedirs(RESULTS_ROOT)

DOWNLOAD_ROOT = os.path.join(
            MEDIA_ROOT, 'items', 'download', ''
            )

if not os.path.exists(DOWNLOAD_ROOT):
    os.makedirs(DOWNLOAD_ROOT)


ROOT_URLCONF = 'urls'

# django-npm
NPM_ROOT_PATH = APP_PATH

STATICFILES_DIRS = ()
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DEBUG': DEBUG,
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Debug Toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'django_filters',
    'timeside.server',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'debug_toolbar',
    'django_celery_results',
    # 'celery.contrib.testing.tasks',
)

# dj A sample logging configuration. The only tangible logging
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
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': "/var/log/app/timeside_debug.log",
            'formatter': 'simple',
        },
    },
    'loggers': {
        'timeside': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'timeside.server.utils.custom_exception_handler',
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    #'PAGE_SIZE': 10
}

CELERY_IMPORTS = ("timeside.server.tasks",)
CELERY_BACKEND_URL = env('REDIS_URL') + '/0'
CELERY_BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = env('REDIS_URL') + '/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_ALWAYS_EAGER = False
# If this is True, all tasks will be executed locally by blocking until the task returns.

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'https://ircam-web.github.io',
    'http://localhost:3000',
]


MESSAGE_BROKER = env('REDIS_URL') + '/1'
COMPLETION_INTERVAL = 10  # blocks

CACHE_RESULT = True

SCHEMA_SERVERS = [
    {
        "url": "https://timeside.ircam.fr/",
        "description": "Production server"
    },
    {
        "url": "https://staging.timeside.ircam.fr/",
        "description": "Staging server"
    },
    {
        "url": "http://localhost:8000/",
        "description": "Local server"
    }
    ]

SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False if env('DEBUG') == 'True' else True

CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = False if env('DEBUG') == 'True' else True

X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x : True
    }

##################
# LOCAL SETTINGS #
##################

TIMESIDE_DEFAULT_DECODER = 'aubio_decoder'


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
