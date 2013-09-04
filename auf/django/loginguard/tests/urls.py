# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^basic_login/$',
        'auf.django.loginguard.tests.views.basic_login',
        {'template_name': 'login.html'},
        name='basic_login'),

    url(r'^guarded_login/$',
        'auf.django.loginguard.tests.views.guarded_login',
        {'template_name': 'login.html'},
        name='guarded_login'),

    url(r'^retry_policy_off_login/$',
        'auf.django.loginguard.tests.views.retry_policy_off_login',
        {'template_name': 'login.html'},
        name='retry_policy_off_login'),

    url(r'^alert_off_login/$',
        'auf.django.loginguard.tests.views.alert_off_login',
        {'template_name': 'login.html'},
        name='alert_off_login'),
    )
