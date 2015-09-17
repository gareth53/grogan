from django.conf.urls import patterns, url
from grogan.apps.assets.admin_views import do_crops

urlpatterns = patterns('',
    url(r'^assetcrop/(?P<asset_id>[0-9]{1,2})/$', do_crops, name="do_crops"),
)
