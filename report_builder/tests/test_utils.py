from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.test import TestCase

from ..utils import (
    get_properties_from_model, get_direct_fields_from_model,
    get_relation_fields_from_model, get_model_from_path_string)
from ..mixins import GetFieldsMixin
from ..models import Report, DisplayField, FilterField
from report_builder_demo.demo_models.models import (
    Bar, Restaurant, Waiter, Comment, Place)


class RelationUtilityFunctionTests(TestCase):
    def test_a_initial_rel_field_name(self):
        """
        Test that the initial assumption about the ManyToOneRel field_name is
        correct
        """
        field_name = (
            Waiter.restaurant.field.rel.field_name
            if hasattr(Waiter.restaurant.field, 'rel')
            else Waiter.restaurant.field.target_field.name
        )
        self.assertEquals(field_name, "place")

    def test_get_relation_fields_from_model_does_not_change_field_name(self):
        """
        Make sure that getting related_fields doesn't overwrite field_name

        Waiter has a ForeignKey to Restaurant.
        The relation from Restaurant to Waiter is a ManyToOneRel object.
        'place' is the PK of Restaurant. The ManyToOneRel field_name should be
        the same at the PK, unless to_field is set on the ForeignKey.

        ManyToManyRel objects are not affected.
        """
        get_relation_fields_from_model(Restaurant)
        field_name = (
            Waiter.restaurant.field.rel.field_name
            if hasattr(Waiter.restaurant.field, 'rel')
            else Waiter.restaurant.field.target_field.name
        )
        self.assertEquals(field_name, "place")
        # Waiter.restaurant.field.rel.get_related_field()


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
            filter_type='contains',
            filter_value='Lots of spam')

    def get_fields_names(self, fields):
        return [field.name for field in fields]

    def test_get_relation_fields_from_model(self):
        fields = get_relation_fields_from_model(Report)
        names = self.get_fields_names(fields)
        self.assertTrue('displayfield' in names or 'report_builder:displayfield' in names)
        self.assertTrue('filterfield' in names or 'report_builder:filterfield' in names)
        self.assertTrue('root_model' in names)
        self.assertEquals(len(names), 7)

    def test_get_model_from_path_string(self):
        result = get_model_from_path_string(Restaurant, 'waiter__name')
        self.assertEqual(result, Waiter)

    def test_get_model_from_path_string_one_to_one(self):
        """Test that one-to-one relationships don't break this function"""
        result = get_model_from_path_string(Restaurant, 'place__serves_pizza')
        self.assertEqual(result, Place)


    def test_get_direct_fields_from_model(self):
        fields = get_direct_fields_from_model(Report)
        names = self.get_fields_names(fields)
        self.assertTrue('created' in names)
        self.assertTrue('description' in names)
        self.assertTrue('distinct' in names)
        self.assertTrue('id' in names)
        self.assertEquals(len(names), 9)

    def test_get_fields(self):
        """ Test GetFieldsMixin.get_fields """
        obj = GetFieldsMixin()
        obj.get_fields(
            Bar,
            "foos",
        )

    def test_get_gfk_fields_from_model(self):
        fields = get_direct_fields_from_model(Comment)

    def test_get_properties_from_model(self):
        properties = get_properties_from_model(DisplayField)
        self.assertEquals(properties[0]['label'], 'choices')
        self.assertEquals(properties[1]['label'], 'choices_dict')

    def test_filter_property(self):
        # Not a very complete test - only tests one type of filter
        result = self.filter_field.filter_property('spam')
        self.assertTrue(result)

    def test_custom_global_model_manager(self):
        """ test for custom global model manager """
        if getattr(settings, 'REPORT_BUILDER_MODEL_MANAGER', False):
            self.assertEquals(
                self.report._get_model_manager(),
                settings.REPORT_BUILDER_MODEL_MANAGER)

    def test_custom_model_manager(self):
        """ test for custom model manager """
        if getattr(
                self.report.root_model.model_class(),
                'report_builder_model_manager',
                True
        ):
            # change setup to use actual field and value
            self.filter_field.field = 'name'
            self.filter_field.filter_value = 'foo'
            self.filter_field.save()
            # coverage of get_query
            objects = self.report.get_query()
            # expect custom manager to return correct object with filters
            self.assertEquals(objects[0], self.report)
