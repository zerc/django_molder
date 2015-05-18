# coding: utf-8
from django import forms


class FormOne(forms.Form):
    """ Exmaple form with several types of fields.
    """
    char_field = forms.CharField(label=u'CharField')

    radio_field = forms.ChoiceField(
        label=u'Radio Choice Field',
        choices=((x, 'choice %s' % x) for x in range(5)))
