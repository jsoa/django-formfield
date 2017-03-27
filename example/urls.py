#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^formfield/', include('formfield.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

#
# urlpatterns = urlpatterns + patterns('',
#     (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT}),
#     ) if settings.DEBUG else urlpatterson
