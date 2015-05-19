# coding: utf-8
from .base import BaseFieldRender, BaseFormRender

__ALL__ = ('FieldRender', 'FormRender', 'MessageRender')


class FieldRender(BaseFieldRender):
    """ Field render
    """


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
