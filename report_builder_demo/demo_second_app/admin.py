from django.contrib import admin
from custom_field.custom_field import CustomFieldAdmin
from .models import Bar


@admin.register(Bar)
class BarAdmin(CustomFieldAdmin, admin.ModelAdmin):
    pass
