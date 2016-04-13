#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from formfield import ModelFormField, FormField


class Coordinates(forms.Form):
    lng = forms.CharField(required=False)
    lat = forms.CharField(required=False)


class Address(forms.Form):
    street = forms.CharField(widget=forms.Textarea)
    country = forms.CharField(required=False)
    zipcode = forms.IntegerField(required=False)

    coords = FormField(Coordinates)


class SubPersonMetaForm(forms.Form):
    middle_name = forms.CharField()
    suffix = forms.CharField(required=False)

    address = FormField(Address)


class PersonMetaForm(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    name = forms.CharField()
    date = forms.DateTimeField(required=False)

    subform = FormField(SubPersonMetaForm)


class Person(models.Model):
    name = models.CharField(max_length=255)

    meta_info = ModelFormField(form=PersonMetaForm)
