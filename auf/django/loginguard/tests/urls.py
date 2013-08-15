# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

from django.contrib import admin
from django.contrib.auth.views import login

from auf.django.loginguard.decorators import login_guard

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^basic_login/$',
        login,
        {'template_name': 'login.html'},
        name='basic_login'),

    url(r'^guarded_login/$',
        login_guard(login),
        {'template_name': 'login.html'},
        name='guarded_login'),

    url(r'^retry_policy_off_login/$',
        login_guard(login),
        {'template_name': 'login.html'},
        name='retry_policy_off_login'),

    url(r'^alert_off_login/$',
        login_guard(login),
        {'template_name': 'login.html'},
        name='alert_off_login'),
    )
