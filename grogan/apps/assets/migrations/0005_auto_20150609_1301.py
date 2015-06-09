# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20150526_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettype',
            name='ratio',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
