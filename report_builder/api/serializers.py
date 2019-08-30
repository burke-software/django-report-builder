from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from report_builder.models import Report, DisplayField, FilterField, Format
from rest_framework import serializers
import datetime

User = get_user_model()


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class DisplayFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayField
        fields = ('id', 'path', 'path_verbose', 'field', 'field_verbose',
                  'name', 'sort', 'sort_reverse', 'width', 'aggregate',
                  'position', 'total', 'group', 'report', 'display_format',
                  'field_type')
        read_only_fields = ('id',)
    
    def to_internal_value(self, data):
        if data.get('sort') is '':
            data['sort'] = None
        return super().to_internal_value(data)


class NonStrictCharField(serializers.CharField):
    """ Allow booleans to be turned into strings instead of erroring """
    def to_internal_value(self, value):
        if value is True:
            return "True"
        elif value is False:
            return "False"
        return super().to_internal_value(value)


class FilterFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterField
        fields = ('id', 'path', 'path_verbose', 'field', 'field_verbose',
                  'field_type', 'filter_type', 'filter_value', 'filter_value2',
                  'exclude', 'position', 'report', 'filter_delta')
        read_only_fields = ('id', 'field_type')

    filter_value = NonStrictCharField(allow_blank=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "id")


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ("pk", "name")


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    root_model = serializers.PrimaryKeyRelatedField(
        queryset=Report.allowed_models())
    root_model_name = serializers.StringRelatedField(source='root_model')
    user_created = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model', 'root_model_name',
                  'user_created')


class ReportNestedSerializer(ReportSerializer):
    displayfield_set = DisplayFieldSerializer(required=False, many=True)
    filterfield_set = FilterFieldSerializer(required=False, many=True)
    user_created = serializers.PrimaryKeyRelatedField(read_only=True)
    user_modified = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id', 'name', 'description', 'modified', 'root_model',
            'root_model_name', 'displayfield_set', 'distinct', 'user_created',
            'user_modified', 'filterfield_set', 'report_file',
            'report_file_creation')
        read_only_fields = ('report_file', 'report_file_creation')

    def validate(self, data):
        if 'filterfield_set' in data:
            for filter_field_data in data['filterfield_set']:
                filter_field = FilterField()
                for key, value in filter_field_data.items():
                    setattr(filter_field, key, value)
                filter_field.clean()
                filter_field_data['filter_value'] = filter_field.filter_value
        return data

    def update(self, instance, validated_data):
        displayfields_data = validated_data.pop('displayfield_set')
        filterfields_data = validated_data.pop('filterfield_set')

        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get(
                'description', instance.description)
            instance.distinct = validated_data.get(
                'distinct', instance.distinct)
            instance.modified = datetime.date.today()
            instance.save()
            instance.displayfield_set.all().delete()
            for displayfield_data in displayfields_data:
                display_field = DisplayField()
                for key, value in displayfield_data.items():
                    setattr(display_field, key, value)
                display_field.save()
            instance.filterfield_set.all().delete()
            for filterfield_data in filterfields_data:
                filter_field = FilterField()
                for key, value in filterfield_data.items():
                    setattr(filter_field, key, value)
                filter_field.save()
        return instance
