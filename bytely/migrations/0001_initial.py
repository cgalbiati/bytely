# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('source_url', models.CharField(max_length=2083)),
                ('short_url', models.CharField(max_length=1000, primary_key=True, serialize=False)),
            ],
        ),
    ]