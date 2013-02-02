# development settings for sprinter
from sprinter.settings.base import *

import os
import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# local development uses local postgres db
DATABASE_URL = 'postgres:///sprinter'

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# not really import for local development
SECRET_KEY = os.environ.get('SECRET_KEY', 'Not that secret')

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

# django-debug-toolbar settings
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'ENABLE_STACKTRACES' : True,
}
