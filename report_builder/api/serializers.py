from django.contrib.contenttypes.models import ContentType
from report_builder.models import Report
from rest_framework import serializers


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    root_model = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all())

    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model')
