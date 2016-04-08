#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import six

from django.db import models
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import striptags
from django.core.exceptions import ValidationError

from .widgets import FormFieldWidget


@six.add_metaclass(models.SubfieldBase)
class JSONField(models.TextField):
    """
    JSONField is a generic textfield that serializes/unserializes
    the data from our form fields
    """

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs',
                                      {'cls': DjangoJSONEncoder})
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        if isinstance(value, six.string_types):
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                pass

        return value

    def get_db_prep_value(self, value, *args, **kwargs):

        if isinstance(value, str):
            return value

        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class FormField(forms.MultiValueField):
    """The form field we can use in forms"""

    def __init__(self, form, **kwargs):
        import inspect
        if inspect.isclass(form) and issubclass(form, forms.Form):
            form_class = form
        elif callable(form):
            form_class = form()
            self.form = form_class()
        elif isinstance(form, six.string_types):
            from django.utils import module_loading
            form_class = module_loading.import_by_path(form)
        self.form = form_class()

        # Set the widget and initial data
        kwargs['widget'] = FormFieldWidget([f for f in self.form])
        kwargs['initial'] = [f.field.initial for f in self.form]

        self.max_length = kwargs.pop('max_length', None)

        super(FormField, self).__init__(**kwargs)

        self.fields = [f.field for f in self.form]

    def compress(self, data_list):
        """
        Return the cleaned_data of the form, everything should already be valid
        """
        data = {}
        if data_list:
            data = dict(
                (f.name, data_list[i]) for i, f in enumerate(self.form))

            f = self.form.__class__(data)
            f.is_valid()
            return f.cleaned_data
        return data

    def clean(self, value):
        """
        Call the form is_valid to ensure every value supplied is valid
        """
        if not value:
            raise ValidationError(
                'Error found in Form Field: Nothing to validate')

        data = dict((bf.name, value[i]) for i, bf in enumerate(self.form))
        self.form = form = self.form.__class__(data)
        if not form.is_valid():
            error_dict = list(form.errors.items())
            errors = striptags(
                ", ".join(["%s (%s)" % (v, k) for k, v in error_dict]))
            raise ValidationError('Error(s) found: %s' % errors)

        # This call will ensure compress is called as expected.
        return super(FormField, self).clean(value)


class ModelFormField(JSONField):
    """The json backed field we can use in our models"""

    def __init__(self, *args, **kwargs):
        """
        This field needs to be nullable and blankable. The supplied form
        will provide the validation.
        """
        self.form = kwargs.pop('form', None)

        kwargs['null'] = True
        kwargs['blank'] = True

        super(ModelFormField, self).__init__(*args, **kwargs)

    def formfield(self, form_class=FormField, **kwargs):
        # Need to supply form to FormField
        return super(ModelFormField, self).formfield(form_class=form_class,
            form=self.form, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^formfield\.fields\.JSONField"])
    add_introspection_rules([], ["^formfield\.fields\.ModelFormField"])
except ImportError:
    pass
