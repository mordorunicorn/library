from .dev import *  # noqa: F401, F403

ENV = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
    },
}
