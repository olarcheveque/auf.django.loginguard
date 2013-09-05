# -*- coding: utf-8 -*-

import time

from django.core.urlresolvers import reverse

from auf.django.loginguard.models import LoginEvent
from auf.django.loginguard import conf

from .common import CommonTest


class LoginTest(CommonTest):

    def setUp(self):
        super(LoginTest, self).setUp()
        self.assertEqual(conf.LOGIN_GUARD_RETRY_POLICY_ON, True)

    def test_basic_login_view(self):
        """
        Check no decorator
        """
        url = reverse('basic_login')

        data = {'username': self.username,
                'password': self.password, }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        data = {'username': self.username,
                'password': 'xxx', }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_guarded_login_view(self):
        """
        Check decorator
        """
        response = self._try_login_ko()
        self.assertEqual(response.status_code, 200)
        #TODO check error message presence

    def test_reactive_on_success(self):
        t1 = time.time()
        response = self._try_login_ko()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all().order_by('-id')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].success, False)
        time.sleep(1)

        # reactive starting date
        response = self._try_login_ok()
        events = LoginEvent.objects.all().order_by('-id')
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].success, True)

        # should be 302 if login start is not reactivated
        response = self._try_login_ko()
        self.assertEqual(response.status_code, 200)
        t2 = time.time()
        # ensure all sequence is done in less than 3s to valid test
        delta = t2 - t1
        self.assertTrue(delta < 3, True)

    def test_retry_policy(self):
        response = self._try_login_ko()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)

        response = self._try_login_ko()
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response['location'])
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)

        time.sleep(3)
        response = self._try_login_ko()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 2)

    def test_fail_event(self):
        self._try_login_ko()
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.who, self.username)
        self.assertEqual(event.host, '127.0.0.1')
        self.assertEqual(event.success, False)
        self.assertTrue(event.when not in ('', None))
        self.assertTrue(self.username in event.__unicode__())
        self.assertTrue('127.0.0.1' in event.__unicode__())
        self.assertTrue('False' in event.__unicode__())

    def test_success_event(self):
        self._try_login_ok()
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.who, self.username)
        self.assertEqual(event.host, '127.0.0.1')
        self.assertEqual(event.success, True)
        self.assertTrue(event.when not in ('', None))
        self.assertTrue(self.username in event.__unicode__())
        self.assertTrue('127.0.0.1' in event.__unicode__())
        self.assertTrue('True' in event.__unicode__())
