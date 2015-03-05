from django.contrib import admin
from custom_field.custom_field import CustomFieldAdmin
from .models import Foo, Bar


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    pass


@admin.register(Bar)
class BarAdmin(CustomFieldAdmin, admin.ModelAdmin):
    pass
