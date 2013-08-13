# -*- coding: utf-8 -*-

import os

USE_I18N = False

SECRET_KEY = 'secret'

ROOT_URLCONF = 'auf.django.loginguard.tests.urls'

DATABASES = {'default':
            {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:', }}

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.admin',
                  'south',
                  'auf.django.loginguard',)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    )
