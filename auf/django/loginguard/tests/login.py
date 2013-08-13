# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User


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
        url = reverse('guarded_login')
        data = {'username': self.username,
                'password': 'xxx', }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
