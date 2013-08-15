# -*- coding: utf-8 -*-

import time

from django.core import mail

from .common import CommonTest


class AlertTest(CommonTest):

    def test_alert_on(self):
        # no alert
        self._try_login_ko()
        mails = [m.body for m in mail.outbox]
        self.assertEqual(len(mails), 0)
        time.sleep(3)
        # alert
        self._try_login_ko()
        mails = [m.body for m in mail.outbox]
        self.assertTrue(u'2 attempts in 0:02:00' in mails)
