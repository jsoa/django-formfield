#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^formfield/', include('formfield.urls')),
    (r'^admin/', include(admin.site.urls)),
)
#
# urlpatterns = urlpatterns + patterns('',
#     (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT}),
#     ) if settings.DEBUG else urlpatterson
