#!/usr/bin/env python

import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)
sys.path[0:0] = [here, parent]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testapp',
    'admin_cli',
)


settings.configure(
    MIDDLEWARE_CLASSES=(),
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
    INSTALLED_APPS=INSTALLED_APPS,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    ROOT_URLCONF='testapp.urls',
    SECRET_KEY="it's a secret to everyone",
    SITE_ID=1,
    SHORT_DATETIME_FORMAT='m/d/Y-H:s',
)


def main():
    if django.VERSION >= (1, 7):
        django.setup()
    if not os.path.exists(os.path.join(here, 'testapp/migrations/0001_initial.py')):
        call_command('makemigrations')
    from django.contrib import admin
    admin.autodiscover()
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner(failfast=True, verbosity=int(os.environ.get('DJANGO_DEBUG', 1)))
    failures = runner.run_tests(['testapp'], interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
