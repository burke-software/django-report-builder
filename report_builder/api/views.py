from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.conf import settings
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


def find_exact_position(fields_list, item):
    current_position = 0
    for i in fields_list:
        if (i.name == item.name and
                i.get_internal_type() == item.get_internal_type()):
            return current_position
        current_position += 1
    return -1


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
        self.model = request.data['model']
        self.path = request.data['path']
        self.path_verbose = request.data.get('path_verbose', '')
        self.field = request.data['field']
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
            included_model = True
            split_name = new_field.name.split(':')
            if len(split_name) == 1:
                split_name.append('')
                split_name[1] = split_name[0]
                split_name[0] = False
                model_information = split_name[1]
            else:
                model_information = split_name[0] + "." + split_name[1]
            app_label = split_name[0]
            model_name = split_name[1]
            if getattr(settings, 'REPORT_BUILDER_INCLUDE', False):
                includes = getattr(settings, 'REPORT_BUILDER_INCLUDE')
                # If it is not included as 'foo' and not as 'demo_models.foo'
                if (model_name not in includes and
                        model_information not in includes):
                    included_model = False
            if getattr(settings, 'REPORT_BUILDER_EXCLUDE', False):
                excludes = getattr(settings, 'REPORT_BUILDER_EXCLUDE')
                # If it is excluded as 'foo' and as 'demo_models.foo'
                if (model_name in excludes or model_information in excludes):
                    included_model = False
            verbose_name = getattr(new_field, 'verbose_name', None)
            if verbose_name is None:
                verbose_name = new_field.get_accessor_name()
            result += [{
                'field_name': new_field.field_name,
                'verbose_name': verbose_name,
                'path': path,
                'help_text': getattr(new_field, 'help_text', ''),
                'model_id': model_ct.id,
                'parent_model_name': model_name,
                'parent_model_app_label': app_label,
                'included_model': included_model,
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

        # External packages might cause duplicates. This clears it up
        new_set = []
        for i in field_data['fields']:
            if i not in new_set:
                new_set.append(i)
        field_data['fields'] = new_set

        result = []
        fields = None
        filters = None
        extra = None
        defaults = None
        meta = getattr(self.model_class, 'ReportBuilder', None)
        if meta is not None:
            fields = getattr(meta, 'fields', None)
            filters = getattr(meta, 'filters', None)
            exclude = getattr(meta, 'exclude', None)
            extra = getattr(meta, 'extra', None)
            defaults = getattr(meta, 'defaults', None)
            if fields is not None:
                fields = list(fields)
                for field in copy.copy(field_data['fields']):
                    if field.name not in fields:
                        index = find_exact_position(
                            field_data['fields'],
                            field
                        )
                        if index != -1:
                            field_data['fields'].pop(index)
            if exclude is not None:
                for field in copy.copy(field_data['fields']):
                    if field.name in exclude:
                        index = find_exact_position(
                            field_data['fields'],
                            field
                        )
                        if index != -1:
                            field_data['fields'].pop(index)
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
                'is_default': True if defaults is None or
                new_field.name in defaults else False,
                'field_choices': new_field.choices,
                'can_filter': True if filters is None or
                new_field.name in filters else False,
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
                if isinstance(field_attr, (property, cached_property)):
                    result += [{
                        'name': field,
                        'field': field,
                        'field_verbose': field,
                        'field_type': 'Property',
                        'field_choices': None,
                        'can_filter': True if filters is None or
                        field in filters else False,
                        'path': field_data['path'],
                        'path_verbose': field_data['path_verbose'],
                        'is_default': True if defaults is None or
                        field in defaults else False,
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
                    'field_choices': field.choices,
                    'can_filter': True if filters is None or
                    field.name in filters else False,
                    'path': field_data['path'],
                    'path_verbose': field_data['path_verbose'],
                    'is_default': True if defaults is None or
                    field.name in defaults else False,
                    'help_text': 'This is a custom field.',
                }]
        return Response(result)


class GenerateReport(DataExportMixin, APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, report_id=None):
        return self.post(request, report_id=report_id)

    def post(self, request, report_id=None):
        report = get_object_or_404(Report, pk=report_id)

        objects_list = report.report_to_list(
            user=request.user,
            preview=True,)
        display_fields = report.get_good_display_fields().values_list(
            'name', flat=True)
        response = {
            'data': objects_list,
            'meta': {'titles': display_fields},
        }

        return Response(response)
