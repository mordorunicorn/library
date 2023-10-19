import dotenv
import dj_database_url
import os
from .base import *  # noqa: F401, F403

ENV = 'prod'

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

ALLOWED_HOSTS = [
    'jessicas-library.herokuapp.com',
    '127.0.0.1',
    '127.0.0.1:8000',
    'localhost',
]

CORS_ORIGIN_WHITELIST = [
    'jessicas-library.herokuapp.com',
    '127.0.0.1',
    '127.0.0.1:8000',
    'localhost',
]

CSRF_COOKIE_SECURE = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'build/static'),
    os.path.join(os.path.dirname(BASE_DIR), 'project', 'staticfiles'),
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARN',
            'class': 'logging.FileHandler',
            'filename': 'log.django',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARN'),
        },
    },
}
