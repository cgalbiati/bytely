# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bytely', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='short_url',
            field=models.CharField(max_length=2000, primary_key=True, serialize=False),
        ),
    ]
