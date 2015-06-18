# coding: utf-8
from django.test import TestCase as DjangoTestCase

from forms import FormOne
from django_molder.renderers import FieldRenderer, FormRenderer

import six


class TestCase(DjangoTestCase):
    """ Common TestCase for renderers tests.
    """
    renderer_cls = None

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()
        cls.form = FormOne()


class CommonTestsMixin(object):
    def test_ivalid_args(self):
        """ Test invalid args for renderer.
        """
        self.assertRaises(ValueError, lambda: self.renderer_cls(None))


class FieldRendererTestCase(TestCase, CommonTestsMixin):
    """ TestCase for `django_molder.renderers.FieldRenderer`
    """
    renderer_cls = FieldRenderer

    def test_char_field_render(self):
        field = self.form['char_field']
        self.__test_some_field_types(field, 'django_molder/common_field.html')

    def test_radio_field_render(self):
        field = self.form['radio_field']
        self.__test_some_field_types(field, 'django_molder/radio_field.html')

    def test_multiple_select_field_render(self):
        field = self.form['multiple_select_field']
        self.__test_some_field_types(
            field,  'django_molder/multiple_checkbox_field.html')

    def test_checkbox_field_render(self):
        field = self.form['checkbox_field']
        self.__test_some_field_types(
            field, 'django_molder/checkbox_field.html')

    def test_file_field_render(self):
        field = self.form['file_field']
        self.__test_some_field_types(field, 'django_molder/file_field.html')

    def __test_some_field_types(self, bound_field, template_name):
        """ Common method for test different form fields.
        """
        renderer = self.renderer_cls(bound_field)

        self.assertEqual(renderer.bound_field, bound_field)

        self.assertEqual(renderer.template, template_name)
        self.assertTrue(isinstance(renderer.render(), six.string_types))

        widget_attrs_as_html = renderer.widget_attrs_as_html
        for attr_name in renderer.widget.attrs.keys():
            self.assertIn(attr_name, widget_attrs_as_html)


class FormRenderedTestCase(TestCase, CommonTestsMixin):
    """ TestCase for `django_molder.renderers.FormRenderer`
    """
    renderer_cls = FormRenderer

    def test_init(self):
        renderer = self.renderer_cls(self.form)

        self.assertEqual(renderer.form, self.form)
        self.assertEqual(renderer.template, 'django_molder/common_form.html')

    def test_render(self):
        renderer = self.renderer_cls(self.form)
        result = renderer.render()

        self.assertTrue(isinstance(renderer.render(), six.string_types))
