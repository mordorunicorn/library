#!/usr/bin/env python
import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))
if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    settings_dir = os.path.join(os.path.dirname(__file__), 'project/settings')
    settings_files = set([f.replace('.py', '') for f in os.listdir(settings_dir)]) - set(
        ('__init__', '__pycache__')
    )

    settings_file = 'prod'

    if sys.argv[1] in settings_files:
        settings_file = sys.argv[1]

    if os.environ.get('DJANGO_ENV') is None:
        os.environ['DJANGO_ENV'] = settings_file

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.{}'.format(settings_file))

    if sys.argv[1] in settings_files:
        execute_from_command_line([sys.argv[0]] + sys.argv[2:])
    else:
        execute_from_command_line(sys.argv)
