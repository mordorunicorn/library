import django_heroku
import dotenv
import dj_database_url
import os
from .base import *  # noqa: F401, F403

ENV = 'prod'

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

django_heroku.settings(locals())

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

ALLOWED_HOSTS = [
    'jessicas-library.herokuapp.com',
    '127.0.0.1:8000',
    'localhost',
]
