from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from model_bakery import baker
from .views import ContentTypeViewSet


User = get_user_model()


class ReportBuilderAPITests(TestCase):
    def test_content_viewset(self):
        factory = APIRequestFactory()
        user = baker.make(User, is_superuser=True, is_staff=True)
        view = ContentTypeViewSet.as_view({'get': 'list'})
        request = factory.get('/report_builder/api/contenttypes/')
        force_authenticate(request, user=user)
        response = view(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, "should return some content types")
