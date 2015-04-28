|BUILD|_

.. |BUILD| image::
   https://secure.travis-ci.org/jsoa/django-formfield.png?branch=master
.. _BUILD: http://travis-ci.org/#!/jsoa/django-formfield


:Version: 0.3
:Docs: https://django-formfield.readthedocs.org/en/latest/
:Download: http://pypi.python.org/pypi/django-formfield/
:Source: https://github.com/jsoa/django-formfield

==========
Change Log
==========

* **0.3**
    * Django 1.6/1.7/1.8 compatibility
    * Python 3.4 compatibility

* **0.2**
    * Fix Django 1.5 install issue

* **0.1.3**
    * Fixed bug when a form's initial value evaludated to ``False``
    * pep8 related fixes

===============
Getting Started
===============

django-formfield is a form field that accepts a django form as its first argument, and validates
as well as render's each form field as expected. Yes a form within a form, *within a dream*? There
are two types of fields available, `FormField` and `ModelFormField`. For
`ModelFormField` the data is stored in json. For `FormField` data is simply
returned as a python dictionary (form.cleaned_data)

============
Installation
============

Installation is easy using ``pip`` or ``easy_install``.

::

	pip install django-formfield

or

::

	easy_install django-formfield


Add to installed apps
=====================

::

    INSTALLED_APPS = (
        ...
        'formfield',
        ...
    )


Example
=======

::

    from django.db import models
    from django import forms

    from formfield import ModelFormField

    class PersonMetaForm(forms.Form):
        age = forms.IntegerField()
        sex = forms.ChoiceField(choices=((1, 'male'), (2, 'female')), required=False)


    class Person(models.Model):
        name = CharField(max_length=200)

        meta_info = ModelFormField(PersonMetaForm)

Which will result in something like this (using the admin)

.. image:: https://github.com/jsoa/django-formfield/raw/master/docs/_images/ss001.png

The `ModelFormField` is automatically set to `null=True`, `blank=True`, this is
because validation is done on the inner form. As a result you will see something like the
following if we hit save on the change form:

.. image:: https://github.com/jsoa/django-formfield/raw/master/docs/_images/ss002.png

If we supply the change for valid data you should get a python dictionary when retrieving
the data::

    >>> person = Person.objects.get(pk=1)
    >>> person.meta_info
    {u'age': 12, u'sex': u'1'}

The form is the only thing forcing valid input, behind the scenes the
data is being serialized into json. Therefore on the python level we can supply meta_info
any valid json:::

    >>> from sample_app.models import Person
    >>> data = {'some': 'thing', 'is': 'wrong', 'here': 'help!'}
    >>> p = Person.objects.create(name="Joan", meta_info=data)
    >>> p.meta_info
    {'is': 'wrong', 'some': 'thing', 'here': 'help!'}

.. note::

    If the form field is being made available via a change form, such as the admin, any
    unexpected value will be overridden by what the form returns . For example, the
    `PersonMetaForm` above only expects `age` and `sex`, so none of the values above
    ('is', 'some' and 'here') match and will be overridden when the form submitted.

    We can however, make the field hidden or readonly and use it to supply any
    valid json, but its not really the intension of this app.
