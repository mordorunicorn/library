from .base import *  # noqa: F401, F403

ENV = 'dev'

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
]
CORS_ALLOW_CREDENTIALS = True
