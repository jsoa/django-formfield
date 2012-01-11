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
        ret = ['<ul class="formfield">']
        for i, field in enumerate(self.fields):
            label = self.format_label(field, i)
            help_text = self.format_help_text(field, i)
            ret.append('<li>%s %s %s</li>' % (
                label, rendered_widgets[i], field.help_text and help_text))
            
        ret.append('</ul>')
        return u''.join(ret)