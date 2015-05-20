from django.conf.urls import patterns, url
from grogan.apps.assets.views import asset_image

urlpatterns = patterns('',
    url(r'^image/(?P<asset_id>[0-9]{1,2})/$', asset_image),
)
