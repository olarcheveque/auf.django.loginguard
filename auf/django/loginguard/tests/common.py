# -*- coding: utf-8 -*-

from django.test import TestCase

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User


class CommonTest(TestCase):

    username = 'paul'
    password = 'lemay'

    def setUp(self):
        self.create_user()

    def create_user(self):
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def _try_login_ko(self):
        data = {'username': self.username,
                'password': 'xxx', }
        url = reverse('guarded_login')
        return self.client.post(url, data)

    def _try_login_ok(self):
        data = {'username': self.username,
                'password': self.password, }
        url = reverse('guarded_login')
        return self.client.post(url, data)
