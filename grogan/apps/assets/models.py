import os
import md5
import re
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Asset categories"


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "People"


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    """
    this could be a country (e.g. UK), city (e.g. London), a venue (e.g. Capital FM Studio)
    it could be a description of the location (e.g. outdoors or space or underground)
    it's just for search, y'know?
    """
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Asset(models.Model):
    """represents a single 'asset', or file, in the system and defines some basic generic metadata"""

    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True)

    image = models.ImageField(upload_to='%Y/%m/%d')

    alt_text = models.CharField(max_length=100)

    # MD5 hash of the file content
    # allows us to 'de-dedupe'
    # TODO - auto-populate this....
    file_hash = models.CharField(max_length=32, blank=True, editable=False)

    # upload details
    # REQUIRED? DO WE ALLOW FOR BLUK UPLOADS VIA AN API IN FUTURE?
    uploaded_by = models.ForeignKey(User, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)

    # attribution information
    author = models.CharField(max_length=255, verbose_name='Attribution', blank=True)
    author_url = models.URLField(verbose_name='Attribution website', blank=True)
    notes = models.TextField(blank = True)

    # in case of copyright-expiration
    do_not_use = models.BooleanField(help_text="This option stops the asset being publically visible!", default=False)

    # multiple choice
    LICENCE_CHOICES = (
        ('unknown', 'Unknown'),
        ('getty', 'Getty'),
        ('getty_free', 'Getty - Royalty Free'),
        ('itn', 'ITN'),
        ('rex', 'Rex'),
        ('commercial', 'Commercial'),
        ('photos_com', 'Photos.com'),
        ('client', 'Client'),
        ('press_release', 'Press Release'),
        ('freelance', 'Freelancer'),
        ('restricted', 'Restricted'),
        ('station', 'Station Owned'),
        ('mms', 'MMS'),
        ('other', 'Other'),
    )
    licence = models.CharField(max_length=1000, choices=LICENCE_CHOICES, default="unknown")

    # metadata
    category = models.ManyToManyField(Category, blank=True)
    people = models.ManyToManyField(Person, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    locations = models.ManyToManyField(Location, blank=True)

#    taken = models.DateField(default=now, help_text="When was this photo taken?")
#       may have to split this into year and month?

    def __unicode__(self):
        return self.title

class Crop(models.Model):

    asset = models.ForeignKey(Asset)
    asset_type = models.ForeignKey('AssetType')

    crop_left = models.IntegerField(default=0)
    crop_top = models.IntegerField(default=0)

    zoom_ratio = models.FloatField(default=1)

    @property
    def crop_bottom(self):
        return self.crop_top + self.asset_type.height

    @property
    def crop_right(self):
        return self.crop_left + self.asset_type.width

    @property
    def width(self):
        return self.asset_type.width

    @property
    def height(self):
        return self.asset_type.height

    def __unicode__(self):
        return "%s (%s x %s)" % (self.asset.title, self.asset_type.width, self.asset_type.height)


class AssetType(models.Model):
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    # ratio = models.DecimalField(max_digits=10, decimal_places=1, default=1)

    def __unicode__(self):
        return "%s [%s x %s]" % (self.name, self.width, self.height)

    def save(self, *args, **kwargs):
        # self.ratio = float(self.width) / self.height
        super(AssetType, self).save(*args, **kwargs)
