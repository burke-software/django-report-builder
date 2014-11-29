from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReportSerializer
from report_builder.models import Report
from report_utils.mixins import GetFieldsMixin


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class RelatedFieldsView(GetFieldsMixin, APIView):
    """ Get related fields from an ORM model
    """
    def get_data_from_request(self, request):
        self.model = request.DATA['model']
        self.path = request.DATA['path']
        self.path_verbose = request.DATA['path_verbose']
        self.field = request.DATA['field']
        self.model_class = ContentType.objects.get(pk=self.model).model_class()

    def post(self, request):
        self.get_data_from_request(request)
        new_fields, model_ct, path = self.get_related_fields(
            self.model_class,
            self.field,
            self.path,
            self.path_verbose,)
        result = []
        for new_field in new_fields:
            verbose_name = getattr(new_field, 'verbose_name', None)
            if verbose_name == None:
                verbose_name = new_field.get_accessor_name()
            result += [{
                'name': new_field.name,
                'verbose_name': verbose_name,

            }]
        return Response(result)

class FieldsView(RelatedFieldsView):
    """ Get direct fields and properties on an ORM model
    """
    def post(self, request):
        self.get_data_from_request(request)
        field_data = self.get_fields(
            self.model_class,
            self.field,
            self.path,
            self.path_verbose,)
        result = []
        for new_field in field_data['fields']:
            verbose_name = getattr(new_field, 'verbose_name', None)
            if verbose_name == None:
                verbose_name = new_field.get_accessor_name()
            result += [{
                'name': new_field.name,
                'verbose_name': verbose_name,

            }]
        return Response(result)
