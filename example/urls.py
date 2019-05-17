#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django

from django.contrib import admin


try:
    from django.urls import path
except (ImportError, ):
    from django.conf.urls import url


major = django.VERSION[0]

admin.autodiscover()


urlpatterns = [
]

if major == 2:
    urlpatterns.append(
        path('admin/', admin.site.urls),
    )
else:
    urlpatterns.append(
        url('^admin/', admin.site.urls)
    )
