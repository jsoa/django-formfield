#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms


class FormFieldWidget(forms.MultiWidget):
    """
    This widget will render each field found in the supplied form.
    """
    def __init__(self, fields, attrs=None):
        self.fields = fields
        # Retreive each field widget for the form
        widgets = [f.field.widget for f in self.fields]

        super(FormFieldWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        """Ensure the payload is a list of values. In the case of a sub
        form, we need to ensure the data is returned as a list and not a
        dictionary.

        When a dict is found in the given data, we need to ensure the data
        is converted to a list perseving the field order.

        """
        if name in data:
            payload = data.get(name)
            if isinstance(payload, (dict,)):
                # Make sure we get the data in the correct roder
                return [payload.get(f.name) for f in self.fields]
            return payload
        return super(FormFieldWidget, self).value_from_datadict(data, files, name)

    def decompress(self, value):
        """
        Retreieve each field value or provide the initial values
        """
        if value:
            return [value.get(field.name, None) for field in self.fields]
        return [field.field.initial for field in self.fields]

    def format_label(self, field, counter):
        """
        Format the label for each field
        """
        return '<label for="id_formfield_%s" %s>%s</label>' % (
            counter, field.field.required and 'class="required"', field.label)

    def format_help_text(self, field, counter):
        """
        Format the help text for the bound field
        """
        return '<p class="help">%s</p>' % field.help_text

    def format_output(self, rendered_widgets):
        """
        This output will yeild all widgets grouped in a un-ordered list
        """
        ret = [u'<ul class="formfield">']
        for i, field in enumerate(self.fields):
            label = self.format_label(field, i)
            help_text = self.format_help_text(field, i)
            ret.append(u'<li>%s %s %s</li>' % (
                label, rendered_widgets[i], field.help_text and help_text))

        ret.append(u'</ul>')
        return ''.join(ret)
