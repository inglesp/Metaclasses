#! from __future__ import print_function
#! import os
#! import sys
#! from prescons.utils import clear_screen
#! from django.conf import settings
#! settings.configure()
#! clear_screen()
###
#
# Advanced Python through Django: Metaclasses
#
# Peter Inglesby
#   @inglesp
#
# 16th May 2013
#
# https://github.com/inglesp/Metaclasses
#
###

# The purpose of this talk is to discuss:
#  - what metaclasses are, and how they work
#  - what they are useful for, and how Django uses them

# Feedback please!

import django

django.get_version()

#! clear_screen()
# Example (i)

from django import forms

class PonyForm(forms.Form):
    name = forms.CharField()
    colour = forms.CharField()
    birthday = forms.DateField()

PonyForm.base_fields
PonyForm.__dict__.keys()


#! clear_screen()
# Example (ii)

from django.db import models

class EquineBase(models.Model):
    class Meta:
        app_label = 'ponies'
        abstrac = True


#! clear_screen()
# Example (iii)

class Stable(models.Model):
    class Meta:
        app_label = 'ponies'
    name = models.CharField()

s = Stable()
s.pony_set

class Pony(models.Model):
    class Meta:
        app_label = 'ponies'
    name = models.CharField()
    stable = models.ForeignKey(Stable)

s.pony_set
Stable.__dict__.keys()


#! clear_screen()
# Classes: a recap

class SomeClass(object):
    class_attr = 123
    def __init__(self, x):
        self.instance_attr = x

instance = SomeClass(123)
type(instance)
type(SomeClass)
isinstance(SomeClass, object)


#! clear_screen()
# We can create classes dynamically

name = 'ExampleClass'
bases = (object,)
attrs = {
    '__init__': lambda self: print('Hello from __init__!')
}
ExampleClass = type(name, bases, attrs)

ExampleClass
type(ExampleClass)
instance = ExampleClass()
instance
type(instance)


#! clear_screen()
# We can control how classes are created

def create_class(name, bases, attrs):
    # We can do anything here!
    return type(name, bases, attrs)


#! clear_screen()
# Example of creating a class dynamically

def create_form_class(name, attrs):
    bases = (object,)
    fields = {k: v for k, v in attrs.items() if isinstance(v, forms.Field)}
    attrs['base_fields'] = fields
    return type(name, bases, attrs)

name = 'PonyForm'
attrs = {
    'name': forms.CharField(),
    'colour': forms.CharField(),
    'birthday': forms.DateField()
}

PonyForm = create_form_class(name, attrs)
PonyForm
PonyForm.base_fields


#! clear_screen()
# Q: What is `type`?

type(type)

# A: `type` itself is a class


#! clear_screen()
# We can subclass `type`

class FormType(type):
    def __new__(cls, name, bases, attrs):
        fields = {k: v for k, v in attrs.items() if isinstance(v, forms.Field)}
        attrs['base_fields'] = fields
        return type.__new__(cls, name, bases, attrs)

name = 'PonyForm'
bases = (object,)
attrs = {
    'name': forms.CharField(),
    'colour': forms.CharField(),
    'birthday': forms.DateField()
}

PonyForm = FormType(name, bases, attrs)
PonyForm
PonyForm.base_fields


#! clear_screen()
# Specifying a metaclass

class Form(object):
    __metaclass__ = FormType

class PonyForm(Form):
    name = forms.CharField()
    colour = forms.CharField()
    birthday = forms.DateField()

PonyForm.__metaclass__
PonyForm.base_fields


#! clear_screen()
# More examples in Django

os.system("cd " + os.path.dirname(django.__file__) + "; grep -r '__metaclass__ =' *")


#! clear_screen()
# Python 3

# class Form(metaclass=Formtype):
#     ...


#! clear_screen()
# The Zen of Python

import this


#! clear_screen()
# Key takeaways:

# * Classes are factories for creating objects
# * Metaclasses are factories for creating classes
# * Metaclasses allow us to control how classes are created


#! clear_screen()
# Dziękuję bardzo!

# Questions?
# Feedback please!
