from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'adalitix',
        'HOST': 'adalitix-postgis',
        'USER': 'adalitix',
        'DATABASE': 'adalitix',
        'PASSWORD': 'adalitix'
    }
}

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
