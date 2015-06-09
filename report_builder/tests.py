from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Report, DisplayField, FilterField, Format
from report_builder_demo.demo_models.models import Bar, Place, Restaurant, Waiter, Person, Child
from django.conf import settings
from report_utils.model_introspection import (
    get_properties_from_model, get_direct_fields_from_model,
    get_relation_fields_from_model, get_model_from_path_string)
from rest_framework.test import APIClient
import time


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
        self.assertEquals(len(names), 6)

    def test_get_model_from_path_string(self):
        result = get_model_from_path_string(Restaurant, 'waiter__name')
        self.assertEqual(result, Waiter)

    def test_get_direct_fields_from_model(self):
        fields = get_direct_fields_from_model(Report)
        names = self.get_fields_names(fields)
        self.assertTrue('created' in names)
        self.assertTrue('description' in names)
        self.assertTrue('distinct' in names)
        self.assertTrue('id' in names)
        self.assertEquals(len(names), 9)

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
        ct = ContentType.objects.get(model="foo")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_fields_from_related(self):
        ct = ContentType.objects.get(model="place")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id,
             "path": "",
             "path_verbose": "",
             "field": "restaurant"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pizza')

    def test_report_builder_exclude(self):
        ct = ContentType.objects.get(model="fooexclude")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_extra(self):
        ct = ContentType.objects.get(model="bar")
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
        ct = ContentType.objects.get(model="bar")
        self.report = Report.objects.create(root_model=ct, name="A")
        self.bar = Bar.objects.create(char_field="wooo")
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
            filter_type='contains',
            filter_value='lol no',
        )
        response = self.client.get(self.generate_url)
        self.assertContains(response, 'lol no')
        filter_field.filter_value = 'It does not contain this'
        filter_field.save()
        response = self.client.get(self.generate_url)
        self.assertNotContains(response, 'lol no')

    def test_filter_custom_field(self):
        from custom_field.models import CustomField
        ct = ContentType.objects.get(model="bar")
        CustomField.objects.create(
            name="custom one",
            content_type=ct,
            field_type="t",
        )
        self.bar.set_custom_value('custom one', 'I am custom')
        DisplayField.objects.create(
            report=self.report,
            field="custom one",
            field_verbose="stuff",
        )
        filter_field = FilterField.objects.create(
            report=self.report,
            field="custom one",
            field_verbose="stuff",
            filter_type='contains',
            filter_value='I am custom',
        )
        response = self.client.get(self.generate_url)
        self.assertContains(response, 'I am custom')
        filter_field.filter_value = 'It does not contain this'
        filter_field.save()
        response = self.client.get(self.generate_url)
        self.assertNotContains(response, 'I am custom')

    def make_lots_of_foos(self):
        for x in range(500):
            bar = Bar.objects.create(char_field="wooo" + str(x))
            bar.foos.create(char_field="a")

    def test_performance(self):
        """ Test getting a report with ORM and property fields.
        Provides baseline on performance testing. """
        self.make_lots_of_foos()
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="char_field",
            field_verbose="stuff",
        )
        start = time.time()
        response = self.client.get(self.generate_url)
        run_time = time.time() - start
        print('report builder report time is {}'.format(run_time))
        self.assertEqual(response.status_code, 200)
        self.assertLess(run_time, 1.0)

    def test_performance_filter(self):
        """ Test getting a report with ORM and property fields.
        Provides baseline on performance testing. """
        self.make_lots_of_foos()
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="char_field",
            field_verbose="stuff",
        )
        FilterField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
            filter_type='contains',
            filter_value='I am custom',
        )
        start = time.time()
        response = self.client.get(self.generate_url)
        run_time = time.time() - start
        print('report builder report time is {}'.format(run_time))
        self.assertEqual(response.status_code, 200)
        self.assertLess(run_time, 1.0)

    def make_tiny_town(self):
        data = [
            ('Golden Gate Bridge', '123 Bridge St, SF, CA', True, True, 4),
            ('Alcatraz Island', '0 Dead Mans Row, SF Bay, CA', True, False, 2),
            ("Fisherman's Warf", 'Pier 39, San Francisco, CA', False, True, 3),
            ('AT&T Park', '3 World Series Way, SF, CA', False, False, 5),
            ('MOMA', '456 Art Avenue, San Francisco, CA', True, True, 8),
        ]

        total = 0

        for row in data:
            place = Place.objects.create(name=row[0], address=row[1])
            restaurant = Restaurant.objects.create(
                place=place, serves_hot_dogs=row[2], serves_pizza=row[3]
            )

            for count in range(row[4]):
                days = None if not (total % 3 | total % 2) else total % 3

                waiter = Waiter.objects.create(
                    restaurant=restaurant,
                    name=str(total),
                    days_worked=days,
                )

                total += 1

    def test_total_accounting(self):
        """ Test accounting total fields.
        Nullable fields should be totalled as 0.
        """
        self.make_tiny_town()

        model = ContentType.objects.get(model='waiter')
        report = Report.objects.create(root_model=model, name='Waiter Days Worked')

        DisplayField.objects.create(
            report=report,
            field='name',
            field_verbose='name_verbose',
            total=True,
        )
        DisplayField.objects.create(
            report=report,
            field='days_worked',
            field_verbose='days_worked_verbose',
            total=True,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        self.assertContains(response, '["TOTALS",""],[22.0,21.0]')

    def make_people(self):
        people = (
            ('John', 'Doe', (
                ('Will', 'Doe', 5, 'R'),
                ('James', 'Doe', 8, ''),
                ('Robert', 'Doe', 3, 'G'),
            )),
            ('Maria', 'Smith', (
                ('Susan', 'Smith', 1, 'Y'),
                ('Karen', 'Smith', 4, 'B'),
            )),
            ('Donald', 'King', (
                ('Mark', 'King', 2, 'B'),
                ('Charles', 'King', None, ''),
                ('Helen', 'King', 7, 'G'),
                ('Lisa', 'King', 3, 'R'),
            )),
            ('Paul', 'Nelson', ()),
        )

        for first_name, last_name, children in people:
            person = Person(first_name=first_name, last_name=last_name)
            person.save()
            for child_first, child_last, age, color in children:
                child = Child(
                    parent=person, first_name=child_first, last_name=child_last,
                    age=age, color=color
                )
                child.save()

    def test_groupby_id(self):
        self.make_people()

        model = ContentType.objects.get(model='child')
        report = Report.objects.create(root_model=model, name='# of Kids / Person Id')

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='id',
            field_verbose="Parent's Id",
            sort=3,
            position=0,
            group=True,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='first_name',
            field_verbose="Parent's First name",
            sort=2,
            sort_reverse=True,
            position=1,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='last_name',
            field_verbose="Parent's Last name",
            sort=1,
            position=2,
        )

        DisplayField.objects.create(
            report=report,
            field='id',
            field_verbose='Child Count',
            sort=4,
            position=3,
            aggregate='Count',
            total=True,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[[1,"John","Doe",3],[3,"Donald","King",4],[2,"Maria","Smith",2],["TOTALS","","",""],["","","",9.0]]'

        self.assertContains(response, data)

    def test_groupby_name(self):
        self.make_people()

        model = ContentType.objects.get(model='child')
        report = Report.objects.create(root_model=model, name='# of Kids / Person Name')

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='id',
            field_verbose="Parent's Id",
            sort=3,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='first_name',
            field_verbose="Parent's First name",
            sort=2,
            sort_reverse=True,
            position=1,
            group=True,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='last_name',
            field_verbose="Parent's Last name",
            sort=1,
            position=2,
            group=True,
            total=True,
        )

        DisplayField.objects.create(
            report=report,
            field='id',
            field_verbose='Child Count',
            sort=4,
            position=3,
            aggregate='Count',
            total=True,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[[1,"John","Doe",3],[3,"Donald","King",4],[2,"Maria","Smith",2],["TOTALS","","",""],["","",3.0,9.0]]'

        self.assertContains(response, data)

    def test_aggregates(self):
        self.make_people()

        model = ContentType.objects.get(model='person')
        report = Report.objects.create(root_model=model, name='Kid Stats')

        DisplayField.objects.create(
            report=report,
            field='first_name',
            field_verbose='First Name',
            sort=1,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            field='last_name',
            field_verbose='Last Name',
            sort=2,
            position=1,
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='age',
            field_verbose='Oldest Age',
            sort=3,
            position=2,
            aggregate='Max',
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='age',
            field_verbose='Youngest Age',
            sort=4,
            position=3,
            aggregate='Min',
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='age',
            field_verbose='Average Age',
            sort=5,
            position=4,
            aggregate='Avg',
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='age',
            field_verbose='Parenting Years',
            sort=6,
            position=5,
            aggregate='Sum',
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["Donald","King",7,2,4.0,12],["John","Doe",8,3,5.333333333333333,16],["Maria","Smith",4,1,2.5,5],["Paul","Nelson",null,null,null,null]]'

        self.assertContains(response, data)

    def test_choices_and_sort_null(self):
        self.make_people()

        model = ContentType.objects.get(model='person')
        report = Report.objects.create(root_model=model, name='Kid Data')

        DisplayField.objects.create(
            report=report,
            field='first_name',
            field_verbose='First Name',
            sort=4,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            field='last_name',
            field_verbose='Last Name',
            sort=3,
            position=1,
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='age',
            field_verbose='Child Age',
            sort=2,
            position=2,
        )

        DisplayField.objects.create(
            report=report,
            path='children__',
            field='color',
            field_verbose='Child Color',
            sort=1,
            position=3,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["Donald","King",null,""],["Paul","Nelson",null,""],["John","Doe",8,""],["Donald","King",2,"Blue"],["Maria","Smith",4,"Blue"],["John","Doe",3,"Green"],["Donald","King",7,"Green"],["Donald","King",3,"Red"],["John","Doe",5,"Red"],["Maria","Smith",1,"Y"]]'

        self.assertContains(response, data)

    def test_formatter(self):
        self.make_people()

        model = ContentType.objects.get(model='child')
        report = Report.objects.create(root_model=model, name='Children')

        DisplayField.objects.create(
            report=report,
            field='first_name',
            field_verbose='First Name',
            sort=1,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            field='last_name',
            field_verbose='Last Name',
            sort=2,
            position=1,
        )

        years_old = Format(name='years old', string='{} years old')
        years_old.save()

        DisplayField.objects.create(
            report=report,
            field='age',
            field_verbose='Child Age',
            sort=3,
            position=2,
            total=True,
            display_format=years_old,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["Charles","King","None years old"],["Helen","King","7 years old"],["James","Doe","8 years old"],["Karen","Smith","4 years old"],["Lisa","King","3 years old"],["Mark","King","2 years old"],["Robert","Doe","3 years old"],["Susan","Smith","1 years old"],["Will","Doe","5 years old"],["TOTALS","",""],["","","33 years old"]]'

        self.assertContains(response, data)

    def test_admin(self):
        response = self.client.get('/admin/report_builder/report/')
        self.assertEqual(response.status_code, 200)
