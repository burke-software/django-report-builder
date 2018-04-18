from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.test import TestCase
from django.test.utils import override_settings
from ..models import (
    Report, DisplayField, FilterField, Format, get_allowed_models,
    get_limit_choices_to_callable)
from report_builder_demo.demo_models.models import (
    Bar, Place, Restaurant, Waiter, Person, Child)
from report_builder.api.serializers import ReportNestedSerializer
from django.conf import settings
from rest_framework.test import APIClient
import time
import csv
import unittest
import json
from io import StringIO
from freezegun import freeze_time
from datetime import date, datetime, timedelta, time as dtime

from django.contrib.auth import get_user_model

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

User = get_user_model()


def find_duplicates_in_contexttype():
    find_duplicates = {}
    duplicates = []
    for i in get_allowed_models():
        model_name = str(i.model)
        if model_name in find_duplicates:
            find_duplicates[model_name] += 1
            duplicates.append(model_name)
        else:
            find_duplicates[model_name] = 1
    return duplicates


class ReportBuilderTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='testy')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password('pass')
        user.save()
        self.client = APIClient()
        self.client.login(username='testy', password='pass')

    def test_get_allowed_models_for_include(self):
        pre_include_duplicates = find_duplicates_in_contexttype()
        settings.REPORT_BUILDER_INCLUDE = (
            'demo_models.bar',
            'demo_models.foo',
            'demo_models.place',
        )
        post_include_duplicates = find_duplicates_in_contexttype()
        settings.REPORT_BUILDER_INCLUDE = None
        self.assertEqual(pre_include_duplicates, ['bar'])
        self.assertEqual(post_include_duplicates, [])

    def test_get_allowed_models_for_exclude(self):
        pre_exclude_duplicates = find_duplicates_in_contexttype()
        settings.REPORT_BUILDER_EXCLUDE = (
            'demo_second_app.bar',
        )
        post_exclude_duplicates = find_duplicates_in_contexttype()
        settings.REPORT_BUILDER_EXCLUDE = None
        self.assertEqual(pre_exclude_duplicates, ['bar'])
        self.assertEqual(post_exclude_duplicates, [])

    def test_get_allowed_models_lookup_dict(self):
        settings.REPORT_BUILDER_INCLUDE = (
            'demo_models.bar',
            'demo_models.foo',
            'demo_models.place',
        )
        models = get_allowed_models()
        lookup_dict = get_limit_choices_to_callable()

        self.assertTrue(callable(get_limit_choices_to_callable))
        self.assertTrue(isinstance(lookup_dict['pk__in'], QuerySet))
        self.assertQuerysetEqual(lookup_dict['pk__in'], map(repr, models), ordered=False)

    def test_report_builder_reports(self):
        url = '/report_builder/api/reports/'
        no_auth_client = APIClient()

        # A non authenticated client cannot view
        response = no_auth_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_report_builder_fields(self):
        ct = ContentType.objects.get(model="foo", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_fields_from_related(self):
        ct = ContentType.objects.get(model="place", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id,
             "path": "",
             "path_verbose": "",
             "field": "restaurant"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pizza')

    def test_report_builder_fields_from_related_with_hidden_field(self):
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id,
             "path": "",
             "path_verbose": "",
             "field": "foos"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_fields_from_related_with_properties(self):
        ct = ContentType.objects.get(model="foo", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id,
             "path": "",
             "path_verbose": "",
             "field": "bar_set"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'i_want_char_field')
        self.assertContains(response, 'i_need_char_field')

    def test_report_builder_fields_from_related_fields(self):
        ct = ContentType.objects.get(model="place", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/related_fields/',
            {"model": ct.id,
             "path": "",
             "path_verbose": "",
             "field": "restaurant"})
        self.assertContains(response, '"parent_model_name"')
        self.assertContains(response, '"parent_model_app_label"')
        self.assertContains(response, '"included_model"')
        self.assertEqual(response.status_code, 200)

    def test_report_builder_exclude(self):
        ct = ContentType.objects.get(model="fooexclude", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertNotContains(response, 'char_field2')

    def test_report_builder_extra(self):
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'char_field')
        self.assertContains(response, 'i_want_char_field')
        self.assertContains(response, 'i_need_char_field')

    def test_report_builder_is_default(self):
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'is_default')

    def test_report_builder_choices(self):
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'field_choices')
        self.assertContains(response, '[["CH","CHECK"],["MA","CHECKMATE"]]')

    def test_report_builder_can_filter(self):
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'can_filter')
        for field in response.data:
            if field['name'] == 'char_field':
                self.assertEqual(field['can_filter'], True)
            else:
                self.assertEqual(field['can_filter'], False)
        # Now confirm not setting filter makes it always true
        ct = ContentType.objects.get(model="foo", app_label="demo_models")
        response = self.client.post(
            '/report_builder/api/fields/',
            {"model": ct.id, "path": "", "path_verbose": "", "field": ""})
        for field in response.data:
            self.assertEqual(field['can_filter'], True)

    def test_report_builder_understands_empty_string(self):
        ct = ContentType.objects.get_for_model(Report)
        report = Report.objects.create(
            name="foo report",
            root_model=ct)

        display_field = DisplayField.objects.create(
            name='foo',
            report=report,
            field="X",
            field_verbose="stuff",
            sort=None,
            position=1)
        data = ReportNestedSerializer(report).data
        data['displayfield_set'][0]['sort'] = ''
        response = self.client.put(f'/report_builder/api/report/{report.id}/',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    HTTP_X_REQUESTED_WWITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(report.displayfield_set.all()[0].sort)

class ReportTests(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='testy')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password('pass')
        user.save()
        self.client = APIClient()
        self.client.login(username='testy', password='pass')
        ct = ContentType.objects.get(model="bar", app_label="demo_models")
        self.report = Report.objects.create(root_model=ct, name="A")
        self.bar = Bar.objects.create(char_field="wooo")
        self.generate_url = reverse('generate_report', args=[self.report.id])
        # time increments in seconds
        self.min = 60
        self.hour = self.min * self.min
        self.day = self.hour * 24

    def test_property_position(self):
        bar = self.bar

        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
            position=1,
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
            position=2,
        )
        report_list = self.report.report_to_list(self.report.get_query())
        self.assertEqual(
            report_list[0],
            [bar.i_want_char_field, bar.i_need_char_field]
        )

    def test_property_and_field_position(self):
        bar = self.bar

        DisplayField.objects.create(
            report=self.report,
            field="char_field",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
        )
        DisplayField.objects.create(
            report=self.report,
            field="char_field",
            field_verbose="stuff",
        )

        report_list = self.report.report_to_list(self.report.get_query())
        self.assertEqual(
            report_list[0],
            [bar.char_field, bar.i_want_char_field, bar.i_need_char_field, bar.char_field]
        )

    def test_property_display(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
        )
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lol no')

    def test_cached_property_display(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
        )
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lol yes')

    def test_error_display_field(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_do_not_exist",
            field_verbose="stuff",
            position=0,
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_want_char_field",
            field_verbose="stuff",
            position=1,
        )
        DisplayField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
            position=2,
        )
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lol no')
        self.assertContains(response, 'lol yes')
        self.assertNotContains(response, 'i_do_not_exist')

    def test_filter_property_contains(self):
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

    def test_filter_cached_property(self):
        DisplayField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
        )
        filter_field = FilterField.objects.create(
            report=self.report,
            field="i_need_char_field",
            field_verbose="stuff",
            filter_type='contains',
            filter_value='lol yes',
        )
        response = self.client.get(self.generate_url)
        self.assertContains(response, 'lol yes')
        filter_field.filter_value = 'It does not contain this'
        filter_field.save()
        response = self.client.get(self.generate_url)
        self.assertNotContains(response, 'lol yes')

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
            field="i_need_char_field",
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

                Waiter.objects.create(
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

        model = ContentType.objects.get(model='waiter', app_label="demo_models")
        report = Report.objects.create(root_model=model, name='Waiter Days Worked')

        DisplayField.objects.create(
            report=report,
            field='name',
            field_verbose='name_verbose',
            total=True,
            position=0,
        )
        DisplayField.objects.create(
            report=report,
            field='days_worked',
            field_verbose='days_worked_verbose',
            total=True,
            position=1,
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        self.assertContains(response, '["TOTALS",""],[22.0,21.0]')

    @freeze_time("2017-11-01 12:00:00")
    def make_people(self):
        """
        Make mock data from the Person and Child demo models.
        Follows the format:
            Person()
                first_name      (CharField)
                last_name       (CharField)
                last_modifed    (DateField)
                birth_date      (DateTimeField)
                hammer_time     (TimeField)
            Child()
                parent          (ForeignKey(Person))
                first_name      (CharField)
                last_name       (CharField)
                age             (IntegerField)
                color           (CharField)
        """
        people = (
            ('John', 'Doe', (
                ('Will', 'Doe', 5, 'R'),
                ('James', 'Doe', 8, ''),
                ('Robert', 'Doe', 3, 'G'),
            ), date.today() - timedelta(seconds=self.day * 5),
                datetime.today() - timedelta(seconds=self.day),
                dtime(hour=12)),
            ('Maria', 'Smith', (
                ('Susan', 'Smith', 1, 'Y'),
                ('Karen', 'Smith', 4, 'B'),
            ), date.today() - timedelta(seconds=self.day * 10),
                datetime.today() - timedelta(seconds=self.day * 30),
                dtime(hour=16)),
            ('Donald', 'King', (
                ('Charles', 'King', None, ''),
                ('Helen', 'King', 7, 'G'),
                ('Mark', 'King', 2, 'Y'),
                ('Karen', 'King', 4, 'R'),
                ('Larry', 'King', 5, 'R'),
                ('Lisa', 'King', 3, 'R'),
            ), datetime.today() - timedelta(seconds=self.day * 15),
                datetime.today() - timedelta(seconds=self.day * 60),
                dtime(hour=20)),
            ('Paul', 'Nelson', (),
                date.today() - timedelta(seconds=self.day * 20),
                datetime.today() - timedelta(seconds=self.day * 90),
                dtime(hour=22)),
        )
        for first, last, cn, lm, bd, ht in people:
            person = Person(
                first_name=first,
                last_name=last,
                last_modifed=lm,  # DateField
                birth_date=bd,  # DateTimeField
                hammer_time=ht)  # TimeField
            person.save()
            for child_first, child_last, age, color in cn:
                child = Child(
                    parent=person, first_name=child_first, last_name=child_last,
                    age=age, color=color
                )
                child.save()

    @freeze_time("2017-11-01 12:00:00")
    def make_people_report(self):
        """
        Make a mock report using the People demo model.

        Creates mock People instances and returns a report including the
        following DisplayFields:
            first_name      (CharField)
            last_modifed    (DateField)
            birth_date      (DateTimeField)
            hammer_time     (TimeField)
        """
        self.make_people()
        model = ContentType.objects.get(model="person",
                                        app_label="demo_models")
        people_report = Report.objects.create(
            root_model=model,
            name="A report of people")

        DisplayField.objects.create(
            report=people_report,
            field='first_name',
            field_verbose='First Name',
            sort=4,
            position=0,
        )

        DisplayField.objects.create(
            report=people_report,
            field='last_modifed',
            field_verbose='Last Modifed',
            sort=2,
            position=2,
        )

        DisplayField.objects.create(
            report=people_report,
            field='birth_date',
            field_verbose='Birth Date',
            sort=1,
            position=3,
        )

        DisplayField.objects.create(
            report=people_report,
            field='hammer_time',
            field_verbose='Hammer Time',
            sort=1,
            position=3,
        )
        return people_report

    @freeze_time("2017-11-01 12:00:00")
    def test_filter_datetime_lte_filter(self):
        """
        Test filtering 'DateTime' field types using simple ORM filtering
        (i.e. filter_type='lte')
        """
        people_report = self.make_people_report()

        # DateField
        ff = FilterField.objects.create(
            report=people_report,
            field='last_modifed',
            filter_type='lte',
            filter_value=str(date.today() - timedelta(seconds=self.day * 10)),
        )

        generate_url = reverse('generate_report', args=[people_report.id])
        response = self.client.get(generate_url)
        # filter from 4 to 2 people
        self.assertEquals(len(response.data['data']), 3)

        # TimeField
        ff.field = 'hammer_time'
        ff.filter_value = str(dtime(hour=13))
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # DateTimeField
        ff.field = 'birth_date'
        ff.filter_value = str(datetime.today() - timedelta(seconds=self.day * 40))
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 2)

    @freeze_time("2017-11-01 12:00:00")
    def test_filter_datetime_range(self):
        """
        Test filtering 'DateTime' field types using a range filter.

        Each FilterField accepts 2 values of the respective field type to
        create the range.

        Ex. Filter a TimeField for 'user logins between 10am - 1pm':
            filter_type='range',
            filter_value("HH:MM") = "10:00"
            filter_value2("HH:MM") = "13:00"
        """
        people_report = self.make_people_report()

        # DateField
        ff = FilterField.objects.create(
            report=people_report,
            field='last_modifed',
            filter_type='range',
            filter_value=str(date.today() - timedelta(seconds=self.day * 7)),
            filter_value2=str(date.today()),
        )

        generate_url = reverse('generate_report', args=[people_report.id])
        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # TimeField
        ff.field = 'hammer_time'
        ff.filter_value = str(dtime(hour=10))
        ff.filter_value2 = str(dtime(hour=13))
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # DateTimeField
        ff.field = 'birth_date'
        ff.filter_value = str(datetime.now() - timedelta(seconds=self.day * 50))
        ff.filter_value2 = str(datetime.now() - timedelta(seconds=self.day * 70))
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

    @freeze_time("2017-11-01 12:00:00")
    def test_filter_datetime_relative_range(self):
        """
        Test filtering 'DateTime' field types using a relative range filter.

        Each FilterField accepts a delta value (in seconds) which represents
        the range (positive or negative) off of the current date.

        Ex. Filter a TimeField for 'user logins in the last 3 hours':
            filter_type='relative_range',
            filter_delta = -60 * 60 * 3 (i.e. 3 hours)
        """
        people_report = self.make_people_report()

        # DateField w/ full day
        ff = FilterField.objects.create(
            report=people_report,
            field='last_modifed',
            filter_type='relative_range',
            filter_delta=self.day * -7,
        )

        generate_url = reverse('generate_report', args=[people_report.id])
        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # DateField w/ partial day
        ff.filter_delta = self.day * -7 + 5
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # TimeField w/ hour delta
        ff.field = 'hammer_time'
        ff.filter_delta = self.hour * 5
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 2)

        # TimeField w/ sec delta
        ff.filter_delta = -5
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

        # DateTimeField w/ full day
        ff.field = 'birth_date'
        ff.filter_delta = self.day * -30
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 2)

        # # DateTimeField w/ partial day
        ff.filter_delta = (self.day + self.hour) * -1
        ff.save()

        response = self.client.get(generate_url)
        self.assertEquals(len(response.data['data']), 1)

    def test_filter_datefield_relative_range_over_time(self):
        """
        Test filtering DateField types using a relative range filter
        over time.
        """
        people_report = self.make_people_report()
        generate_url = reverse('generate_report', args=[people_report.id])

        initial_today = datetime(2017, 11, 1, 12)
        ten_days_later = datetime(2017, 11, 10, 12)

        # DateField with login 'today'
        with freeze_time(initial_today) as frozen_today:
            FilterField.objects.create(
                report=people_report,
                field='last_modifed',
                filter_type='relative_range',
                filter_delta=self.day * -16,
            )
            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 3)

            # login again 10 days later
            frozen_today.move_to(ten_days_later)
            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 1)

    def test_filter_timefield_relative_range_over_time(self):
        """
        Test filtering TimeField field types using a relative range filter
        over time.
        """

        people_report = self.make_people_report()
        generate_url = reverse('generate_report', args=[people_report.id])

        initial_today = datetime(2017, 11, 1, 12)
        four_hours_later_today = datetime(2017, 11, 1, 16)

        # TimeField with login 'now'
        with freeze_time(initial_today) as frozen_today:
            FilterField.objects.create(
                report=people_report,
                field='hammer_time',
                filter_type='relative_range',
                filter_delta=self.hour * -10,
            )
            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 1)

            # login 4 hours later
            frozen_today.move_to(four_hours_later_today)
            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 2)

    def test_filter_datetimefield_relative_range_over_time(self):
        """
        Test filtering DateTimeField field types using a relative range filter
        over time.
        """
        people_report = self.make_people_report()
        generate_url = reverse('generate_report', args=[people_report.id])

        initial_today = datetime(2017, 10, 1, 12)
        one_month_later = datetime(2017, 11, 1, 12)

        # DateTimeField with login today
        with freeze_time(initial_today) as frozen_today:
            FilterField.objects.create(
                report=people_report,
                field='birth_date',
                filter_type='relative_range',
                filter_delta=self.day * -30
            )

            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 1)

            # # login one month later
            frozen_today.move_to(one_month_later)
            response = self.client.get(generate_url)
            self.assertEquals(len(response.data['data']), 2)

    def test_groupby_id(self):
        self.make_people()

        model = ContentType.objects.get(model='child', app_label="demo_models")
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

        data = '"data":[[1,"John","Doe",3],[3,"Donald","King",6],[2,"Maria","Smith",2],["TOTALS","","",""],["","","",11.0]]'

        self.assertContains(response, data)

    def test_groupby_name(self):
        self.make_people()

        model = ContentType.objects.get(model='child', app_label="demo_models")
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

        data = '"data":[[1,"John","Doe",3],[3,"Donald","King",6],[2,"Maria","Smith",2],["TOTALS","","",""],["","",3.0,11.0]]'

        self.assertContains(response, data)

    def test_aggregates(self):
        self.make_people()

        model = ContentType.objects.get(model='person', app_label="demo_models")
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

        data = '"data":[["Donald","King",7,2,4.2,21],["John","Doe",8,3,5.333333333333333,16],["Maria","Smith",4,1,2.5,5],["Paul","Nelson",null,null,null,null]]'

        self.assertContains(response, data)

    @unittest.skip('Broken in 1.10')
    def test_choices_and_sort_null(self):
        self.make_people()

        model = ContentType.objects.get(model='person', app_label="demo_models")
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

        FilterField.objects.create(
            report=report,
            field='first_name',
            filter_type='exact',
            filter_value='Donald',
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["Donald","King",null,""],["Donald","King",7,"Green"],["Donald","King",3,"Red"],["Donald","King",4,"Red"],["Donald","King",5,"Red"],["Donald","King",2,"Y"]]'

        self.assertContains(response, data)

    def test_formatter(self):
        self.make_people()

        model = ContentType.objects.get(model='child', app_label="demo_models")
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

        FilterField.objects.create(
            report=report,
            path='parent__',
            field='first_name',
            filter_type='exact',
            filter_value='Maria',
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["Karen","Smith","4 years old"],["Susan","Smith","1 years old"],["TOTALS","",""],["","","5 years old"]]'

        self.assertContains(response, data)

    def test_csv(self):
        self.make_people()

        model = ContentType.objects.get(model='child', app_label="demo_models")
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

        settings.REPORT_BUILDER_ASYNC_REPORT = False
        download_csv = reverse('report_download_file', args=[report.id, 'csv'])
        response = self.client.get(download_csv)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'][1], 'text/csv')
        csv_string = response._container[0]
        f = StringIO(csv_string.decode('UTF-8'))
        reader = csv.reader(f, delimiter=',')
        csv_list = list(reader)
        self.assertEqual(csv_list[1], ['Charles', 'King', 'None years old'])

    def test_admin(self):
        response = self.client.get('/admin/report_builder/report/')
        self.assertEqual(response.status_code, 200)

    @override_settings(REPORT_BUILDER_ASYNC_REPORT=False)
    def test_admin_sync(self):
        response = self.client.get('/admin/report_builder/report/')
        self.assertEqual(response.status_code, 200)

    def test_report_builder_related_fields(self):
        '''
        Test for Django 1.8 support via
        https://github.com/burke-software/django-report-builder/issues/144
        '''
        ct = ContentType.objects.get(model='place')
        response = self.client.post(
            '/report_builder/api/related_fields/', {
                'model': ct.id,
                'path': '',
                'field': 'restaurant'
            }
        )
        self.assertContains(response, '"field_name":"waiter"')
        self.assertContains(response, '"verbose_name":"waiter_set"')
        self.assertContains(response, '"path":"restaurant__"')

    def test_annotation_filter_min(self):
        """
        Similar to group-by queries, annotation-filters allow you to display only
        the Max or Min of a set of rows.

        Suppose we have two models, Person and Child. Each has first_name,
        last_name fields and Child has a foreign key to Person as parent. Child
        also has age and color fields. Already we can use the group-by
        mechanism to display each Person's count of children or the age of each
        person's oldest child.

        Unfortunately, getting the related items of an aggregate is difficult
        in Django and SQL. Suppose in the example above that we want to know
        the name and age of each person's oldest child. With annotation-filters
        this can be done.

        Annotation-filters are applied iteratively after normal queryset
        filtering. They work, as the name indicates, by applying Django's
        annotate and filter queryset methods. As they are self-referential,
        they do not accept a text input from the front-end.

        Annotation-filters are difficult to describe conceptually so I'll use
        an example. To display the name and age of each person's oldest child,
        we begin by constructing a report based on Child. We add display fields
        for the parent name, child name, and child age. Then for filter fields,
        we add the parent__children__age field. This lengthy path indicates
        that children are to be grouped by their parent and with the type Max,
        only the maximum age of each group should be included.
        """
        self.make_people()

        model = ContentType.objects.get(model='child')
        report = Report.objects.create(root_model=model, name="Person's Youngest Child")

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='first_name',
            field_verbose="Person First name",
            sort=2,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='last_name',
            field_verbose="Person Last name",
            sort=1,
            position=1,
        )

        DisplayField.objects.create(
            report=report,
            field='first_name',
            field_verbose='Child First Name',
            sort=4,
            position=2,
        )

        DisplayField.objects.create(
            report=report,
            field='last_name',
            field_verbose='Child Last Name',
            sort=3,
            position=3,
        )

        DisplayField.objects.create(
            report=report,
            field='age',
            field_verbose='Child Age',
            position=4,
        )

        FilterField.objects.create(
            report=report,
            path='parent__children__',
            field='age',
            filter_type='min',
            filter_value='True',
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["John","Doe","Robert","Doe",3],["Donald","King","Mark","King",2],["Maria","Smith","Susan","Smith",1]]'

        self.assertContains(response, data)

    def test_annotation_filter_max(self):
        """
        See test_annotation_filter_min for a description of annotation-filters.

        This test extends things further by adding the filter field
        parent__children__color with type Equals Red to get a list of the
        oldest children of each person whose favorite color is red.
        """
        self.make_people()

        model = ContentType.objects.get(model='child')
        report = Report.objects.create(root_model=model, name="Person's Oldest Child whose Favorite Color is Red")

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='first_name',
            field_verbose="Person First name",
            sort=2,
            position=0,
        )

        DisplayField.objects.create(
            report=report,
            path='parent__',
            field='last_name',
            field_verbose="Person Last name",
            sort=1,
            position=1,
        )

        DisplayField.objects.create(
            report=report,
            field='first_name',
            field_verbose='Child First Name',
            sort=4,
            position=2,
        )

        DisplayField.objects.create(
            report=report,
            field='last_name',
            field_verbose='Child Last Name',
            sort=3,
            position=3,
        )

        DisplayField.objects.create(
            report=report,
            field='age',
            field_verbose='Child Age',
            position=4,
        )

        FilterField.objects.create(
            report=report,
            path='parent__children__',
            field='color',
            filter_type='exact',
            filter_value='R',
        )

        FilterField.objects.create(
            report=report,
            path='parent__children__',
            field='age',
            filter_type='max',
            filter_value='True',
        )

        generate_url = reverse('generate_report', args=[report.id])
        response = self.client.get(generate_url)

        data = '"data":[["John","Doe","Will","Doe",5],["Donald","King","Larry","King",5]]'

        self.assertContains(response, data)

    def test_get_config(self):
        settings.REPORT_BUILDER_ASYNC_REPORT = True
        response = self.client.get('/report_builder/api/config/')
        self.assertContains(response,'"async_report": true')
