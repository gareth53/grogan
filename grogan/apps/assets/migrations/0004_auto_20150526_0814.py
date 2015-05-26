# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_crop_asset_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='crop_bottom',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='crop_right',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='height',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='ratio',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='width',
        ),
        migrations.AddField(
            model_name='assettype',
            name='ratio',
            field=models.DecimalField(default=1, max_digits=10, decimal_places=1),
            preserve_default=False,
        ),
    ]
