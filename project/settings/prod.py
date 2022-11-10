import django_heroku
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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

django_heroku.settings(locals())
