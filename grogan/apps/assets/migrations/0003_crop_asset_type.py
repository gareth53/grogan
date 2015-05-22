# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_assettype'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='asset_type',
            field=models.ForeignKey(default=1, to='assets.AssetType'),
            preserve_default=False,
        ),
    ]
