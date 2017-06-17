# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 00:46
from __future__ import unicode_literals

from django.db import migrations


def load_data(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "initial")


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
