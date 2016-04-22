from __future__ import unicode_literals

from django.db import models


class Url(models.Model):
    source_url = models.CharField(max_length=2083) # max length of a url
    short_url = models.CharField(primary_key=True,max_length=2000) # leave room for host url
    def __str__(self):
        return self.source_url

