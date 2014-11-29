from report_builder.models import Report
from rest_framework import serializers


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    root_model = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = Report
        fields = ('id', 'name', 'modified', 'root_model')

