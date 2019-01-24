from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import json


class ApiTestCase(TestCase):

    def setUp(self):
        self.su = get_user_model().objects.create_superuser('su', 'su@example.com', 'su')
        self.client = APIClient()

    def get_child_related_fields(self):
        self.client.login(username='su', password='su')
        ct = ContentType.objects.get_by_natural_key('demo_models', 'child')
        response = self.client.post(
            reverse('related_fields'),
            {'field': '', 'model': ct.id, 'path': ''},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        return content

    def test_related_fields(self):
        related_fields = self.get_child_related_fields()
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertTrue(related_fields[0]['included_model'])

    @override_settings(REPORT_BUILDER_EXCLUDE=['demo_models.person'])
    def test_related_fields_exclude(self):
        related_fields = self.get_child_related_fields()
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertFalse(related_fields[0]['included_model'])

    def get_content_types(self):
        self.client.login(username='su', password='su')
        response = self.client.get('/report_builder/api/contenttypes/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        return content

    def test_get_all_content_types(self):
        num_content_types = ContentType.objects.count()
        response = self.get_content_types()
        self.assertEqual(len(response), num_content_types)

    @override_settings(REPORT_BUILDER_EXCLUDE=['demo_models.person'])
    def test_get_content_types_with_exclude(self):
        num_content_types = ContentType.objects.count()
        response = self.get_content_types()
        self.assertEqual(len(response), num_content_types - 1)
