#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from setuptools import setup, find_packages
import formfield


def read_file(filename):
    """Read a file into a string"""
    p = path.abspath(path.dirname(__file__))
    filepath = path.join(p, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if path.exists(name):
            return read_file(name)
    return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(formfield.__doc__.splitlines()).strip()

setup(
    name="django-formfield",
    version=formfield.get_version().replace(' ', '-'),
    url='http://github.com/jsoa/django-formfield/',
    author='Jose Soares',
    author_email='jose@linux.com',
    description=DESC,
    long_description=get_readme(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_file('requirements.txt'),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Django',
    ],
)
