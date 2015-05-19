# coding: utf-8
from django import forms
from django.conf import settings


MOLDER_DEFAULT_CLASSES_FOR_WIDGETS = \
    getattr(settings, 'MOLDER_DEFAULT_CLASSES_FOR_WIDGETS', {
        None: '',  # default
        forms.TextInput: 'form-control',
        forms.ClearableFileInput: 'fileinput',
    })
