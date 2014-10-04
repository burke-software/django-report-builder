from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client
from .models import Report, DisplayField
from .views import *
from django.conf import settings
from report_utils.model_introspection import get_properties_from_model, get_direct_fields_from_model

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
        self.assertEquals(len(names), 9)

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
            cf = CustomField.objects.create(
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
        result = filter_property(self.filter_field, 'spam')
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


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'temporary@example.com', 'user')
        self.user.is_staff = True
        self.user.save()
        self.c = Client()
        self.c.login(username="user", password="user")
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

    def test_ajax_get_related(self):
        response = self.c.get('/report_builder/ajax_get_related/', {
            'field': 'user_created',
            'model': self.report_ct.id,
            'path': '',
            'path_verbose': '',
            })
        self.assertContains(response, "report_starred_set")
        self.assertContains(response, "user_permissions")
        self.assertContains(response, "report_modified_set")

    def test_ajax_get_fields(self):
        response = self.c.get('/report_builder/ajax_get_fields/', {
            'model': self.report_ct.id,
            'field': 'displayfield',
            'path': '',
            'path_verbose': '',
            })
        self.assertContains(response, 'data-name="aggregate"')
        self.assertContains(response, 'data-path="displayfield__"')
        self.assertContains(response, "field")
        self.assertContains(response, "field verbose")
        self.assertContains(response, "group")
        self.assertContains(response, "ID [AutoField]")
        self.assertContains(response, "name [CharField]")
        self.assertContains(response, "path [CharField]")

