from django.contrib.contenttypes.models import ContentType
from report_builder.models import Report, DisplayField, FilterField
from rest_framework import serializers


class DisplayFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayField


class FilterFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterField


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    root_model = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all())
    root_model_name = serializers.StringRelatedField(source='root_model')

    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model', 'root_model_name')


class ReportNestedSerializer(ReportSerializer):
    displayfield_set = DisplayFieldSerializer(required=False, many=True)

    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model', 'root_model_name',
                  'displayfield_set',)
