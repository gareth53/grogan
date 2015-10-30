# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.core.management import call_command

fixture = 'initial_data'

def load_fixture(apps, schema_editor):

    call_command('loaddata', fixture, app_label='assets') 

def unload_fixture(apps, schema_editor):
	print "This Migrations has no reverse!"

class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
		migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]