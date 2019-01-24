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
        return response

    def test_related_fields(self):
        response = self.get_child_related_fields()
        related_fields = json.loads(response.content)
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertTrue(related_fields[0]['included_model'])

    @override_settings(REPORT_BUILDER_EXCLUDE=['demo_models.person'])
    def test_related_fields_exclude(self):
        response = self.get_child_related_fields()
        related_fields = json.loads(response.content)
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertFalse(related_fields[0]['included_model'])
