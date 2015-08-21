# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to=b'%Y/%m/%d')),
                ('alt_text', models.CharField(max_length=100)),
                ('file_hash', models.CharField(max_length=32, editable=False, blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('author', models.CharField(max_length=255, verbose_name=b'Attribution', blank=True)),
                ('author_url', models.URLField(verbose_name=b'Attribution website', blank=True)),
                ('notes', models.TextField(blank=True)),
                ('do_not_use', models.BooleanField(default=False, help_text=b'This option stops the asset being publically visible!')),
                ('licence', models.CharField(default=b'unknown', max_length=1000, choices=[(b'unknown', b'Unknown'), (b'getty', b'Getty'), (b'getty_free', b'Getty - Royalty Free'), (b'itn', b'ITN'), (b'rex', b'Rex'), (b'commercial', b'Commercial'), (b'photos_com', b'Photos.com'), (b'client', b'Client'), (b'press_release', b'Press Release'), (b'freelance', b'Freelancer'), (b'restricted', b'Restricted'), (b'station', b'Station Owned'), (b'mms', b'MMS'), (b'other', b'Other')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Asset categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crop_left', models.IntegerField(default=0)),
                ('crop_top', models.IntegerField(default=0)),
                ('zoom_ratio', models.FloatField(default=1)),
                ('asset', models.ForeignKey(to='assets.Asset')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CropSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b"Something generic e.g. 'Small square'", max_length=100)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'People',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='crop',
            name='crop_spec',
            field=models.ForeignKey(to='assets.CropSize'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='category',
            field=models.ManyToManyField(to='assets.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='groups',
            field=models.ManyToManyField(to='assets.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='locations',
            field=models.ManyToManyField(to='assets.Location', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='people',
            field=models.ManyToManyField(to='assets.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
