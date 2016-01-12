from django.conf.urls import patterns, url
from .views import demo

urlpatterns = patterns('',
    url(r'^demo/(?P<asset_id>[0-9]+)/$', demo, name="demo"),
)
