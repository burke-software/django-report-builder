from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from .models import Report, DisplayField, FilterField
from .views import *
from report_builder_demo.demo_models.models import *
from django.conf import settings
from report_utils.model_introspection import (
    get_properties_from_model, get_direct_fields_from_model,
    get_relation_fields_from_model)
from rest_framework.test import APIClient


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class UtilityFunctionTests(TestCase):
    def setUp(self):
        self.report_ct = ContentType.objects.get_for_model(Report)
        self.report = Report.objects.create(
            name="foo report",
            root_model=self.report_ct)
        self.filter_field = FilterField.objects.create(
            report=self.report,
            field="X",
            field_verbose="stuff",
            filter_type = 'contains',
            filter_value = 'Lots of spam')

    def get_fields_names(self, fields):
        names = []
        for field in fields:
            names += [field.name]
        return names

    def test_get_relation_fields_from_model(self):
        fields = get_relation_fields_from_model(Report)
        names = self.get_fields_names(fields)
        self.assertTrue('report_builder:displayfield' in names)
        self.assertTrue('report_builder:filterfield' in names)
        self.assertTrue('root_model' in names)
        self.assertEquals(len(names), 6)

    def test_get_direct_fields_from_model(self):
        fields = get_direct_fields_from_model(Report)
        names = self.get_fields_names(fields)
        self.assertTrue('created' in names)
        self.assertTrue('description' in names)
        self.assertTrue('distinct' in names)
        self.assertTrue('id' in names)
        self.assertEquals(len(names), 9)

    def test_get_custom_fields_from_model(self):
        if 'custom_field' in settings.INSTALLED_APPS:
            from custom_field.models import CustomField
            CustomField.objects.create(
                name="foo",
                content_type=self.report_ct,
                field_type='t',)
            fields = get_custom_fields_from_model(Report)
            self.assertEquals(fields[0].__class__, CustomField)
            self.assertEquals(fields[0].name, "foo")

    def test_get_properties_from_model(self):
        properties = get_properties_from_model(DisplayField)
        self.assertEquals(properties[0]['label'], 'choices')
        self.assertEquals(properties[1]['label'], 'choices_dict')

    def test_filter_property(self):
        # Not a very complete test - only tests one type of filter
        result = self.filter_field.filter_property('spam')
        self.assertTrue(result)

    def test_custom_global_model_manager(self):
        #test for custom global model manager
        if getattr(settings, 'REPORT_BUILDER_MODEL_MANAGER', False):
            self.assertEquals(self.report._get_model_manager(), settings.REPORT_BUILDER_MODEL_MANAGER)

    def test_custom_model_manager(self):
        #test for custom model manager
        if getattr(self.report.root_model.model_class(), 'report_builder_model_manager', True):
            #change setup to use actual field and value
            self.filter_field.field = 'name'
            self.filter_field.filter_value = 'foo'
            self.filter_field.save()
            #coverage of get_query
            objects, message = self.report.get_query()
            #expect custom manager to return correct object with filters
            self.assertEquals(objects[0], self.report)


class ReportBuilderTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='testy')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password('pass')
        user.save()
        self.client = APIClient()
        self.client.login(username='testy', password='pass')

    def test_report_builder_fields(self):
        ct = ContentType.objects.get(name="foo")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_exclude(self):
        ct = ContentType.objects.get(name="foo exclude")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_extra(self):
        ct = ContentType.objects.get(name="bar")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertContains(response, 'i_want_char_field')


class ReportTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='testy')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password('pass')
        user.save()
        self.client = APIClient()
        self.client.login(username='testy', password='pass')
        ct = ContentType.objects.get(name="bar")
        self.report = Report.objects.create(root_model=ct, name="A")
        Bar.objects.create(char_field="wooo")
        self.generate_url = reverse('generate_report', args=[self.report.id])

    def test_property_display(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lol no')

    def test_error_display_field(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_do_not_exist",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lol no')
        self.assertNotContains(response, 'i_do_not_exist')

    def test_filter_property(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        filter_field = FilterField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
            filter_type = 'contains',
            filter_value = 'lol no',
        )
        response = self.client.get(self.generate_url)
        self.assertContains(response, 'lol no')
        filter_field.filter_value = 'It does not contain this'
        filter_field.save()
        response = self.client.get(self.generate_url)
        self.assertNotContains(response, 'lol no')
