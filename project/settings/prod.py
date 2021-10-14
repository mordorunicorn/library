from .base import *  # noqa: F401, F403
from . import settings_secrets

ENV = 'prod'

SECRET_KEY = settings_secrets.SECRET_KEY

DEBUG = False
