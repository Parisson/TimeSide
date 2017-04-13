from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'timeside',
    }
} 

ROOT_URLCONF = 'timeside.server.urls'
