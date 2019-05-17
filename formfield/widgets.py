#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe


class FormFieldWidget(forms.MultiWidget):
    """
    This widget will render each field found in the supplied form.
    """

    template_name = 'django/forms/widgets/formfield.html'

    class Media:
        css = {
            'all': ('css/formfield.css', )
        }

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
        if field.field.widget.is_hidden:
            return ''
        required = field.field.required and 'class="required"' or ''
        return mark_safe('<label for="id_formfield_%s" %s>%s</label>' % (
            counter, required, field.label))

    def format_help_text(self, field, counter):
        """
        Format the help text for the bound field
        """
        help_text = mark_safe('<p class="help">%s</p>' % field.help_text)
        is_visible = not field.field.widget.is_hidden
        return (help_text and is_visible and help_text) or ''

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

    def get_context(self, name, value, attrs):
        context = super(FormFieldWidget, self).get_context(name, value, attrs)

        # Add in the missing labels and help_text, since we are rendering
        # a subform, we need to show the field names per input
        for i, sub in enumerate(context['widget']['subwidgets']):
            sub['label'] = self.format_label(self.fields[i], i)
            sub['help_text'] = self.format_help_text(self.fields[i], i)

        return context
