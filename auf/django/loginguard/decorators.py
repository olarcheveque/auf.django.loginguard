# -*- coding: utf-8 -*-

from django.contrib import messages


from .guard import LoginGuard, StressLoginException
from .conf import LOGIN_GUARD_RETRY_POLICY_ON


def login_guard(view_login):
    """
    Decorator to apply prevent from brute force.
    """
    if LOGIN_GUARD_RETRY_POLICY_ON is False:
        return view_login

    def _wrapped_view(request, *args, **kwargs):
        from .views import redirect_to_login
        guard = LoginGuard(request)
        try:
            guard.check()  # prevent login perform
            response = view_login(request, *args, **kwargs)
            guard.log()
            guard.check()  # recheck to warn user
        except StressLoginException, e:
            messages.add_message(request, messages.ERROR, e)
            redirect_field_name = kwargs.get('redirect_fieldname')
            redirect_to = request.REQUEST.get(redirect_field_name)
            return redirect_to_login(request, next=redirect_to)

        return response
    return _wrapped_view
