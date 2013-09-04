# -*- coding: utf-8 -*-


from .guard import LoginGuard, StressLoginException

import conf


def login_guard(view_login):
    """
    Decorator to apply prevent from brute force.
    """
    if conf.LOGIN_GUARD_RETRY_POLICY_ON is False:
        return view_login

    def _wrapped_view(request, *args, **kwargs):
        if request.method not in ('POST', ):
            return view_login(request, *args, **kwargs)

        guard = LoginGuard(request)
        try:
            guard.check()  # prevent login perform
            response = view_login(request, *args, **kwargs)
            guard.log()
            guard.notify_user()
            return response
        except StressLoginException:
            guard.notify_user()
            from django.contrib.auth.views import redirect_to_login
            redirect_field_name = kwargs.get('redirect_fieldname')
            redirect_to = request.REQUEST.get(redirect_field_name)
            return redirect_to_login(
                next=redirect_to,
                redirect_field_name=redirect_field_name)

    return _wrapped_view
