from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import (
    ReportNestedSerializer, ReportSerializer, FormatSerializer,
    FilterFieldSerializer)
from report_builder.models import Report, Format, FilterField
from report_utils.mixins import GetFieldsMixin, DataExportMixin
import copy


class FormatViewSet(viewsets.ModelViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer
    pagination_class = None


class FilterFieldViewSet(viewsets.ModelViewSet):
    queryset = FilterField.objects.all()
    serializer_class = FilterFieldSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = None


class ReportNestedViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportNestedSerializer
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user_created=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_modified=self.request.user)


class RelatedFieldsView(GetFieldsMixin, APIView):
    """ Get related fields from an ORM model
    """
    permission_classes = (IsAdminUser,)
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
    permission_classes = (IsAdminUser,)
    def post(self, request):
        self.get_data_from_request(request)
        field_data = self.get_fields(
            self.model_class,
            self.field,
            self.path,
            self.path_verbose,)
        result = []
        fields = None
        extra = None
        meta = getattr(self.model_class, 'ReportBuilder', None)
        if meta is not None:
            fields = getattr(meta, 'fields', None)
            exclude = getattr(meta, 'exclude', None)
            extra = getattr(meta, 'extra', None)
            if fields is not None:
                fields = list(fields)
                for field in copy.copy(field_data['fields']):
                    if field.name not in fields:
                        field_data['fields'].remove(field)
            if exclude is not None:
                for field in copy.copy(field_data['fields']):
                    if field.name in exclude:
                        field_data['fields'].remove(field)
            if extra is not None:
                extra = list(extra)

        for new_field in field_data['fields']:
            verbose_name = getattr(new_field, 'verbose_name', None)
            if not verbose_name:
                verbose_name = new_field.get_accessor_name()
            result += [{
                'name': new_field.name,
                'field': new_field.name,
                'field_verbose': verbose_name,
                'field_type': new_field.get_internal_type(),
                'path': field_data['path'],
                'path_verbose': field_data['path_verbose'],
                'help_text': new_field.help_text,
            }]
        # Add properties
        if fields is not None or extra is not None:
            if fields and extra:
                extra_fields = list(set(fields + extra))
            elif fields is not None:
                extra_fields = fields
            else:
                extra_fields = extra
            for field in extra_fields:
                field_attr = getattr(self.model_class, field, None)
                if isinstance(field_attr, property):
                    result += [{
                        'name': field,
                        'field': field,
                        'field_verbose': field,
                        'field_type': 'Property',
                        'path': field_data['path'],
                        'path_verbose': field_data['path_verbose'],
                        'help_text': 'Adding this property will '
                        'significantly increase the time it takes to run a '
                        'report.'
                    }]
        # Add custom fields
        custom_fields = field_data.get('custom_fields', None)
        if custom_fields:
            for field in custom_fields:
                result += [{
                    'name': field.name,
                    'field': field.name,
                    'field_verbose': field.name,
                    'field_type': 'Custom Field',
                    'path': field_data['path'],
                    'path_verbose': field_data['path_verbose'],
                    'help_text': 'This is a custom field.',
                }]
        return Response(result)


class GenerateReport(DataExportMixin, APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, report_id=None):
        return self.post(request, report_id=report_id)

    def post(self, request, report_id=None):
        report = get_object_or_404(Report, pk=report_id)
        user = request.user
        queryset = report.get_query()

        display_fields = report.get_good_display_fields()
        property_filters = []
        for field in report.filterfield_set.all():
            if field.field_type in ["Property", "Custom Field"]:
                property_filters += [field]

        objects_list, message = self.report_to_list(
            queryset,
            display_fields,
            user,
            property_filters=property_filters,
            preview=True,)
        display_fields = display_fields.values_list('name', flat=True)
        response = {
            'data': objects_list,
            'meta': {'titles': display_fields},
        }

        return Response(response)
