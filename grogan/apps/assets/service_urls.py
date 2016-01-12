from django.conf.urls import patterns, url
from grogan.apps.assets.views import asset_image, asset_search

urlpatterns = patterns('',
    url(r'^image/(?P<asset_id>[0-9]{1,2})/$', asset_image),
    url(r'^search/$', asset_search),
)
