.. _api:

===
API
===

.. _api_formfield:

FormField
=========

A form field which accepts a `django.forms.Form` as the first argument.
:ref:`api_widget_formfield` is used as this fields widget.

Example Usage::

    from django import forms
    from formfield import FormField
    
    class OtherInfoForm(forms.Form):
        other_name = forms.CharField()
        
    
    class MyForm(forms.Form):
        
        name = forms.CharField()
        
        other_info = FormField(OtherInfoForm)
        
    
Seems odd to have a form within a form yea? Its more useful when using it with 
a model where the data is saved in json format.


.. _api_model_formfield:

ModelFormField
==============

A model form field which accepts a `django.forms.Form` as the first argument. 
:ref:`api_formfield` is used as form field.


Example Usage::

    from django.db import models
    from django import forms
    from formfield import ModelFormField
    
    class MetaDataForm(forms.Form):
        alias = forms.CharField(required=False)
        phone = forms.CharField(required=False)
        email = forms.EmailField(required=False)
        
    
    class Contact(models.Model):
        
        name = models.CharField(max_length=200)
        
        meta_data = ModelFormField(MetaDataForm)
    

.. _api_widget_formfield:

FormFieldWidget
===============

This is the widget used to render the output in a user friendly way. We added 
some methods to help render the output. The main method to override is the normal 
`format_output`, here is the default code::

    ret = ['<ul class="formfield">']
    for i, field in enumerate(self.fields):
        label = self.format_label(field, i)
        help_text = self.format_help_text(field, i)
        ret.append('<li>%s %s %s</li>' % (
            label, rendered_widgets[i], field.help_text and help_text))
            
    ret.append('</ul>')
    return u''.join(ret)
    
It simply wraps the entire form in a <ul> tag with a css class of `formfield`, you 
can override this for more control.

Extra methods
-------------

FormFieldWidget.format_label
****************************

FormFieldWidget.format_help_text
********************************

If you don't want to override the entire method you can override `format_label` and 
`format_help_text` as well. These methods accept to arguments, the bound field and 
a counter::

    def format_label(self, field, counter):
        return '<label for="id_formfield_%s" %s>%s</label>' % (
            counter, field.field.required and 'class="required"', field.label)
            
    def format_help_text(self, field, counter):
        return '<p class="help">%s</p>' % field.help_text