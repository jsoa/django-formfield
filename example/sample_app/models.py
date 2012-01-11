from django.db import models
from django import forms

from formfield import ModelFormField, FormField

class PersonMetaForm1(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    
class PersonMetaForm2(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm1)
    
class PersonMetaForm3(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm2)
    
class PersonMetaForm4(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm3)
    
class PersonMetaForm5(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm4)
    
class PersonMetaForm6(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm5)
    
class PersonMetaForm7(forms.Form):
    age = forms.IntegerField()
    sex = forms.ChoiceField(required=False, choices=((1, 'male'), (2, 'female')))
    
    more = FormField(PersonMetaForm6)
    

class Person(models.Model):
    name = models.CharField(max_length=255)
    
    meta_info = ModelFormField(PersonMetaForm7)