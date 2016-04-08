#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Person


admin.site.register(Person)
