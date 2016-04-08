#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from formfield import ModelFormField


class PersonMetaForm(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))


class Person(models.Model):
    name = models.CharField(max_length=255)

    meta_info = ModelFormField(form=PersonMetaForm)
