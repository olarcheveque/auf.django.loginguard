# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.core.mail import mail_admins
from django.utils.translation import ugettext as _

from django.contrib import messages

from .models import LoginEvent
import conf


class StressLoginException(Exception):
    """
    Exception when you perform too much login attempts according
    retry policy.
    """

    def __init__(self, attempts=None, period=None, waiting_time=None):
        self.attempts = attempts
        self.period = period
        self.waiting_time = waiting_time

    def __unicode__(self):
        return _("""You tried to login %s times in %s.\
 Please wait %s. Thank you.""") % (
            self.attempts,
            timedelta(seconds=self.period),
            timedelta(seconds=self.waiting_time),
            )


class LoginGuard(object):
    """
    Protect and alert about login attempts.
    """

    request = None
    who = None
    host = None

    def __init__(self, request):
        if request.method != 'POST':
            raise Exception('Guard works with POST')  # pragma: no cover

        self.request = request
        self.who = self.request.POST.get('username')
        self.host = self.request.META.get('REMOTE_ADDR', 'unknown')

    def alert(self):
        """
        Send a mail alert to admins according frequency alerts.
        """
        if not conf.LOGIN_GUARD_FREQUENCY_ALERT_ON:
            return
        now = datetime.now()
        for period, attempts in conf.LOGIN_GUARD_FREQUENCY_ALERT:
            start_time = now - timedelta(seconds=period)
            nb_events = LoginEvent.objects.\
                filter(who=self.who, when__gt=start_time).\
                count()
            if nb_events >= attempts:
                subject = u"%s: %s" % (_('alert login attempts'), self.who)
                message = u"%s %s %s" % (
                    nb_events,
                    _('attempts in'),
                    timedelta(seconds=period))
                mail_admins(subject, message)

    def is_valid_according_policy(self):
        now = datetime.now()
        retry_policy = sorted(
            conf.LOGIN_GUARD_RETRY_POLICY,
            key=lambda rule: rule[0],
            reverse=True)

        # get older period
        start_time = now - timedelta(seconds=retry_policy[0][0])

        # build event list based on the max range, if there is a success
        # authentication, the range starts from this one.
        max_events = LoginEvent.objects.\
            filter(who=self.who, when__gt=start_time).\
            order_by('-when')
        events = []
        for e in max_events:
            if e.success:
                break
            else:
                events.append(e)

        for period, attempts in retry_policy:
            check_before = timedelta(seconds=period)
            start_time = now - check_before
            period_events = [e for e in events if e.when >= start_time]
            if len(period_events) >= attempts:
                elapsed = (now - period_events[0].when).seconds
                waiting_time = period - elapsed
                raise StressLoginException(
                    len(period_events),
                    period,
                    waiting_time)

    def check(self,):
        """
        Check if the login attempt respect the retry policy
        """
        self.is_valid_according_policy()

    def notify_user(self,):
        if self.request.user.is_anonymous():
            try:
                self.is_valid_according_policy()
            except StressLoginException, e:
                    messages.add_message(self.request, messages.ERROR, e)

    def log(self,):
        """
        Create a loginevent after login attempt result.
        """
        if self.request.user.is_anonymous():
            self.fail()
        else:
            self.success()
        self.alert()

    def success(self,):
        LoginEvent(who=self.who, host=self.host, success=True).save()

    def fail(self,):
        LoginEvent(who=self.who, host=self.host, success=False).save()
