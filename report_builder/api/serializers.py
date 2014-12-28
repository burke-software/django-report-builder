from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from report_builder.models import Report, DisplayField, FilterField
from rest_framework import serializers
import datetime


class DisplayFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplayField
        read_only_fields = ('id',)


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
                  'displayfield_set', 'distinct')

    def update(self, instance, validated_data):
        displayfields_data = validated_data.pop('displayfield_set')

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
        return instance
