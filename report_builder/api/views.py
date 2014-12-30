from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ReportNestedSerializer, ReportSerializer, FormatSerializer,
    FilterFieldSerializer)
from report_builder.models import Report, Format, FilterField
from report_utils.mixins import GetFieldsMixin, DataExportMixin


class FormatViewSet(viewsets.ModelViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class FilterFieldViewSet(viewsets.ModelViewSet):
    queryset = FilterField.objects.all()
    serializer_class = FilterFieldSerializer
    

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportNestedViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportNestedSerializer

    def perform_create(self, serializer):
        serializer.save(user_created=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_modified=self.request.user)


class RelatedFieldsView(GetFieldsMixin, APIView):
    """ Get related fields from an ORM model
    """
    def get_data_from_request(self, request):
        self.model = request.DATA['model']
        self.path = request.DATA['path']
        self.path_verbose = request.DATA.get('path_verbose', '')
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
                'field_name': new_field.field_name,
                'verbose_name': verbose_name,
                'path': path,
                'help_text': getattr(new_field, 'help_text', ''),
                'model_id': model_ct.id,
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
                'field': new_field.name,
                'field_verbose': verbose_name,
                'path': field_data['path'],
                'path_verbose': field_data['path_verbose'],
                'help_text': new_field.help_text,
            }]
        return Response(result)


class GenerateReport(DataExportMixin, APIView):
    def get(self, request, report_id=None, format=None, queryset=None):
        return self.post(request, report_id=report_id)

    def post(self, request, report_id=None, format=None, queryset=None):
        report = get_object_or_404(Report, pk=report_id)
        user = request.user
        if not queryset:
            queryset, message = report.get_query()
        property_filters = report.filterfield_set.filter(
            Q(field_verbose__contains='[property]') |
            Q(field_verbose__contains='[custom')
        )
        objects_list, message = self.report_to_list(
            queryset,
            report.displayfield_set.all(),
            user,
            property_filters=property_filters,
            preview=False,)
        display_fields = report.displayfield_set.all().values_list('name', flat=True)
        response = {
            'data': objects_list,
            'meta': {'titles': display_fields},
        }

        return Response(response)
