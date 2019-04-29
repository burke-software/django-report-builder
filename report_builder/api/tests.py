from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import json


class ApiTestCase(TestCase):

    def setUp(self):
        um = get_user_model()
        self.superuser = um.objects.create_superuser('su', 'su@example.com', 'su')
        self.regularuser = um.objects.create_user('user', 'user@example.com', 'user')
        self.client = APIClient()

    def get_json(self, url):
        self.client.login(username='su', password='su')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        return content

    def post_json(self, url, data):
        response = self.client.post(
            url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        return content

    def test_endpoint_not_accessable_by_regular_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get('/report_builder/api/contenttypes/')
        self.assertEqual(response.status_code, 403)

    def get_related_fields_for_ct(self, app_label, model_name):
        self.client.login(username='su', password='su')
        ct = ContentType.objects.get_by_natural_key(app_label, model_name)
        content = self.post_json(
            reverse('related_fields'),
            {'field': '', 'model': ct.id, 'path': ''},
        )
        return content

    def test_related_fields(self):
        related_fields = self.get_related_fields_for_ct('demo_models', 'child')
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertTrue(related_fields[0]['included_model'])

    @override_settings(REPORT_BUILDER_EXCLUDE=['demo_models.person'])
    def test_related_fields_exclude(self):
        related_fields = self.get_related_fields_for_ct('demo_models', 'child')
        self.assertEqual(len(related_fields), 1)
        self.assertEqual(related_fields[0]['field_name'], 'parent')
        self.assertFalse(related_fields[0]['included_model'])

    def test_get_all_content_types(self):
        num_content_types = ContentType.objects.count()
        response = self.get_json('/report_builder/api/contenttypes/')
        self.assertEqual(len(response), num_content_types)

    @override_settings(REPORT_BUILDER_EXCLUDE=['demo_models.person'])
    def test_get_content_types_with_exclude(self):
        num_content_types = ContentType.objects.count()
        response = self.get_json('/report_builder/api/contenttypes/')
        self.assertEqual(len(response), num_content_types - 1)
