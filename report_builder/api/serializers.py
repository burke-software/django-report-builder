from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.contrib.auth import get_user_model
from report_builder.models import Report, DisplayField, FilterField, Format
from rest_framework import serializers
import datetime

User = get_user_model()


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format


class DisplayFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayField
        read_only_fields = ('id',)


class FilterFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterField
        read_only_fields = ('id',)


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    root_model = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all())
    root_model_name = serializers.StringRelatedField(source='root_model')

    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model', 'root_model_name')


class ReportNestedSerializer(ReportSerializer):
    displayfield_set = DisplayFieldSerializer(required=False, many=True)
    filterfield_set = FilterFieldSerializer(required=False, many=True)
    user_created = serializers.PrimaryKeyRelatedField(read_only=True)
    user_modified = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id', 'name', 'modified', 'root_model', 'root_model_name',
            'displayfield_set', 'distinct', 'user_created', 'user_modified',
            'filterfield_set', 'report_file', 'report_file_creation')
        read_only_fields = ('report_file', 'report_file_creation')

    def update(self, instance, validated_data):
        displayfields_data = validated_data.pop('displayfield_set')
        filterfields_data = validated_data.pop('filterfield_set')

        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.distinct = validated_data.get('distinct', instance.distinct)
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
