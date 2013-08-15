# -*- coding: utf-8 -*-

import time

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User

from auf.django.loginguard.models import LoginEvent


class LoginTest(TestCase):

    client = Client()
    username = 'paul'
    password = 'lemay'

    def setUp(self):
        self.create_user()

    def create_user(self):
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_basic_login_view(self):
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
        data = {'username': self.username,
                'password': 'xxx', }
        url = reverse('guarded_login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def _try_login(self):
        data = {'username': self.username,
                'password': 'xxx', }
        url = reverse('guarded_login')
        return self.client.post(url, data)

    def test_retry_policy(self):
        response = self._try_login()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)

        response = self._try_login()
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response['location'])
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 1)

        time.sleep(3)
        response = self._try_login()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 2)

    def test_flag_policy(self):
        response = self._try_login()
        self.assertEqual(response.status_code, 200)
        events = LoginEvent.objects.all()
        self.assertEqual(len(events), 0)
