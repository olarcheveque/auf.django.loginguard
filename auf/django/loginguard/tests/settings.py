# -*- coding: utf-8 -*-

import os

ADMINS = ('sample@ut.org', )

USE_I18N = False

SECRET_KEY = 'secret'

ROOT_URLCONF = 'auf.django.loginguard.tests.urls'

LOGIN_URL = '/guarded_login/'

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

LOGIN_GUARD_RETRY_POLICY_ON = True

LOGIN_GUARD_RETRY_POLICY = (
    (1, 1),  # 1 times allowed in 1s
    (3, 2),  # 2 times allowed in 3s
    )

LOGIN_GUARD_FREQUENCY_ALERT_ON = True

LOGIN_GUARD_FREQUENCY_ALERT = (
    (60*2, 2),  # alert if 2 attempts for same user within 2min
    )
