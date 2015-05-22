# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
