#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from .fields import ModelFormField, FormField


class MetaForm(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(
        required=False, choices=((1, 'Make'), (2, 'Female')))


class Coordinates(forms.Form):
    lng = forms.CharField(required=False)
    lat = forms.CharField(required=False)


class Address(forms.Form):
    street = forms.CharField()
    country = forms.CharField(required=False)
    zipcode = forms.IntegerField(required=False)

    coords = FormField(Coordinates)


class PersonForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    suffix = forms.CharField(required=False)
    age = forms.IntegerField(required=False)

    address = FormField(Address)


class TestModel(models.Model):
    name = models.CharField(max_length=255)
    meta_data = ModelFormField(MetaForm)

    personal = ModelFormField(PersonForm)


class FormFieldTests(TestCase):
    """
    Tests for django-formfield
    """
    maxDiff = None

    def setUp(self):
        self.model = TestModel.objects.create(
            name="John",
            meta_data={'age': 32, 'sex': 1})

    def test_01_get_field(self):
        """Ensure the data is a proper dictionary"""
        self.assertEqual(self.model.meta_data, {'age': 32, 'sex': 1})

    def test_02_modify_field(self):
        """After a change is made, ensure the data is still a dictionary"""
        self.model.meta_data = {'age': 18, 'sex': 2}
        self.model.save()
        self.assertEqual(self.model.meta_data, {'age': 18, 'sex': 2})

        # Ensure we can also pass set a string representation of the json
        self.model.meta_data = '{"age": 15, "sex": 1}'
        self.model.save()
        self.assertEqual(self.model.meta_data, {'age': 15, 'sex': 1})

    def test_03_formfield(self):
        """Ensure the field cleans properly"""
        initial_data = {'age': 23, 'sex': 1}
        field = FormField(MetaForm, initial=initial_data)

        # A multi-value field will receive the values as a list
        # in the correct order of the form
        self.assertEqual(field.clean([10, 1]), {'age': 10, 'sex': '1'})

        self.assertRaises(ValidationError, field.clean, [])

    def test_04_form(self):
        """
        Ensure a django form with the form field is valid if supplied with the
        correct data
        """
        class MyForm(forms.Form):
            name = forms.CharField()
            meta_data = FormField(MetaForm)

        form = MyForm()
        self.assertFalse(form.is_valid())

        # We need to supply the django form with the proper multi value
        # data i.e. <field>_0 <field>_1 that represent each (inner) form field
        form = MyForm({'name': 'john', 'meta_data_0': 12, 'meta_data_1': 1})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        # Ensure the cleaned data is what we expect
        self.assertEqual(form.cleaned_data,
            {'name': 'john', 'meta_data': {'age': 12, 'sex': '1'}})

        class MyFormToo(forms.Form):
            name = forms.CharField()
            meta_data = FormField('formfield.tests.MetaForm')

        form = MyFormToo()
        self.assertFalse(form.is_valid())

        form = MyFormToo({'name': 'john', 'meta_data_0': 12, 'meta_data_1': 1})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        # Ensure the cleaned data is what we expect
        self.assertEqual(form.cleaned_data,
            {'name': 'john', 'meta_data': {'age': 12, 'sex': '1'}})

        class MyFormThree(forms.Form):
            name = forms.CharField()
            meta_data = FormField(lambda: MetaForm)

        form = MyFormThree()
        self.assertFalse(form.is_valid())

        form = MyFormThree({'name': 'john', 'meta_data_0': 12, 'meta_data_1': 1})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        # Ensure the cleaned data is what we expect
        self.assertEqual(form.cleaned_data,
            {'name': 'john', 'meta_data': {'age': 12, 'sex': '1'}})

    def test_05_sub_formfield(self):
        """Ensure sub formfields validate"""
        payload = {
            'first_name': '1',
            'last_name': '2',
            'suffix': '3',
            'age': 4,
            'address': {
                'street': '5',
                'country': '6',
                'zipcode': 7,
                'coords': {
                    'lng': '8',
                    'lat': '9'
                    }
                }
            }
        field = FormField(PersonForm)
        data_to_clean = ['1', '2', '3', '4', ['5', '6', '7', ['8', '9']]]
        self.assertEqual(field.clean(data_to_clean), payload)

    def test_06_invalidate_required_subform_field(self):
        """Ensure a proper validation error is raised with sub formfield is
        invalid (required field)"""

        field = FormField(PersonForm)
        # Invalidate a required field (street)
        data_to_clean = ['1', '2', '3', '4', [None, '6', '7', ['8', '9']]]
        self.assertRaises(ValidationError, field.clean, data_to_clean)

    def test_07_invalidate_int_subform_field(self):
        """Ensure a proper validation error is raised with sub formfield is
        invalid (integer only)"""
        field = FormField(PersonForm)
        # Invalidate a integer field (zipcode)
        data_to_clean = ['1', '2', '3', '4', ['5', '6', 'aaa', ['8', '9']]]
        self.assertRaises(ValidationError, field.clean, data_to_clean)
