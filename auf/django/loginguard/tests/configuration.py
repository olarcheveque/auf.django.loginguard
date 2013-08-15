# -*- coding: utf-8 -*-

import time

from django.core import mail
from django.core.urlresolvers import reverse

from auf.django.loginguard.models import LoginEvent

from .common import CommonTest


class SettingTest(CommonTest):

    def _try_patched_login_ko(self, url_name):
        data = {'username': self.username,
                'password': 'xxx', }
        url = reverse(url_name)
        return self.client.post(url, data)

    def test_flag_policy(self):
        """
        no timecheck if flag is off, no log
        """
        response = self._try_patched_login_ko('retry_policy_off_login')
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 0)
        response = self._try_patched_login_ko('retry_policy_off_login')
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 0)

    def test_alert(self):
        """
        no timecheck if flag is off, no log
        """
        self._try_patched_login_ko('alert_off_login')
        time.sleep(3)
        self._try_patched_login_ko('alert_off_login')
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 2)
        mails = [m.body for m in mail.outbox]
        self.assertEqual(len(mails), 0)
