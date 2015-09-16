from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/assets/', include('grogan.apps.assets.admin_urls')),
    url(r'^api/1.0/assets/', include('grogan.apps.assets.service_urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
