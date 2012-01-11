from django.test import TestCase
from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from .fields import ModelFormField, FormField

class MetaForm(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'Make'), (2, 'Female')))
    

class TestModel(models.Model):
    name = models.CharField(max_length=255)
    
    meta_data = ModelFormField(MetaForm)
    

class FormFieldTests(TestCase):
    """
    Tests for django-formfield
    """
    def setUp(self):
        self.model = TestModel.objects.create(
            name="John", meta_data={'age': 32, 'sex': 1})
    
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
        