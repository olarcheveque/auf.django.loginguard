# -*- coding: utf-8 -*-

from django.contrib.auth.views import login

from auf.django.loginguard.decorators import login_guard


def basic_login(*args, **kwargs):
    return login(*args, **kwargs)


@login_guard
def guarded_login(*args, **kwargs):
    return login(*args, **kwargs)


@login_guard
def retry_policy_off_login(*args, **kwargs):
    return login(*args, **kwargs)


@login_guard
def alert_off_login(*args, **kwargs):
    return login(*args, **kwargs)
