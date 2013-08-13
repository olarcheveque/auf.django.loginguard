# -*- coding: utf-8 -*-

from django.db import models


class LoginEvent(models.Model):
    """Record login attempt"""
    when = models.DateTimeField(auto_now=True)
    who = models.CharField(max_length=80)
    host = models.CharField(max_length=25)
    success = models.BooleanField()

    def __unicode__(self):
        return u"|".join((
            str(self.when),
            str(self.success),
            self.who,
            self.host,
            ))
