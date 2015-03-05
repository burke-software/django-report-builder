from django.contrib import admin
from custom_field.custom_field import CustomFieldAdmin
from .models import Foo, Bar


@admin.register(Foo)
class FooAdmin(CustomFieldAdmin, admin.ModelAdmin):
    pass


admin.site.register(Bar)
