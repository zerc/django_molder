# coding: utf-8
import re

from django import forms
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.contrib.messages import get_messages, constants
from django.utils.translation import ugettext as _

import six

__ALL__ = ('FieldRender',)


class BaseFieldRender(object):
    """ Base field render class
    """
    def __init__(self, bound_field, label_class='', show_help=True,
                 show_label=True, help_on_top=False,
                 template=None, hide_form_col=False,
                 required=None,
                 **kwargs):
        self.bound_field = bound_field
        self.field = bound_field.field
        self.widget = bound_field.field.widget
        self.kwargs = kwargs
        self.bound_field_value = bound_field.value()

        self.template = template
        self.template_args = dict(
            label_class=label_class, show_help=show_help,
            show_label=show_label, help_on_top=help_on_top,
            hide_form_col=hide_form_col,
            required=[required, self.field.required][required is None]
        )

    def render(self):
        self.patch_widget_attrs()

        context = {'bound_field': self.bound_field, 'field': self.field,
                   'bound_field_value': self.bound_field_value,
                   'renderer': self}
        context.update(self.template_args)

        return render_to_string(self.template, context)

    def patch_widget_attrs(self):
        self.widget.attrs.setdefault('class', '')
        self.widget.attrs['class'] += self.default_class_for_widget

        # TODO: make hooks for differenrs field classes

        specified_class = self.kwargs.pop('class', None)
        if specified_class:
            if specified_class[0] == '+':
                self.widget.attrs['class'] += ' {}'.format(specified_class[1:])
            else:
                self.widget.attrs['class'] = specified_class

        self.widget.attrs['class'] = self.widget.attrs['class'].strip()

        for a_name, a_value in self.kwargs.items():
            a_name = a_name.replace('data_', 'data-')
            self.widget.attrs[a_name] = a_value

    # TODO: move it into settings
    @property
    def default_class_for_widget(self):
        if isinstance(self.widget, forms.FileInput):
            return ' accountFormCol__text-fileinput'

        if isinstance(self.widget,
                      (forms.CheckboxInput, forms.CheckboxSelectMultiple,
                       forms.RadioSelect)):
            return ' accountFormCol__checkbox'

        return ' form-control'

    @property
    def template(self):
        if self._template:
            return self._template

        if isinstance(self.widget, forms.RadioSelect):
            return 'molder/radio_field.html'

        if isinstance(self.widget, forms.CheckboxSelectMultiple):
            return 'molder/multiple_checkbox_field.html'

        if isinstance(self.widget, forms.CheckboxInput):
            return 'molder/checkbox_field.html'

        if isinstance(self.widget, forms.FileInput):
            return 'molder/file_field.html'

        return 'molder/common_field.html'

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def widget_attrs_as_html(self):
        return mark_safe(u' '.join('{}="{}"'.format(k, v) for k, v in
                                   self.widget.attrs.items()))


class FieldRender(BaseFieldRender):
    """ Field render
    """


class BaseFormRender(object):
    """ Base form render class
    """
    def __init__(self, form, form_template=None, **kwargs):
        if not isinstance(form, forms.BaseForm):
            raise ValueError(u'Invalid form class')

        self.form = form
        self.kwargs = kwargs
        self.template = form_template

    def render(self, *args, **kwargs):
        context = {'form': self.form, 'rendered_fields': self.rendered_fields}
        return render_to_string(self.template, context)

    @property
    def rendered_fields(self):
        for bound_field in self.form:
            yield FieldRender(bound_field, **self.kwargs).render()

    @property
    def template(self):
        if self._template:
            return self._template
        return 'molder/common_form.html'

    @template.setter
    def template(self, value):
        self._template = value


class FormRender(BaseFormRender):
    """ Form render
    """


class MessageRender(object):
    """ Render for django messages framework.
    """
    def __init__(self, request, template=None, **kwargs):
        self.request = request
        self.template = template

    def render(self, *args, **kwargs):
        context = {'messages': self.get_messages()}
        return render_to_string(self.template, context)

    def get_messages(self):
        for message in get_messages(self.request):
            yield message, message.level in (constants.SUCCESS, constants.INFO)

    @property
    def template(self):
        if self._template:
            return self._template
        return 'molder/messages.html'

    @template.setter
    def template(self, value):
        self._template = value
