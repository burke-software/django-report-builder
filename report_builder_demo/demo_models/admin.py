from django.contrib import admin
from custom_field.custom_field import CustomFieldAdmin
from .models import Foo, Bar, Place, Waiter, Restaurant


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    pass


@admin.register(Bar)
class BarAdmin(CustomFieldAdmin, admin.ModelAdmin):
    pass


admin.site.register(Place)
admin.site.register(Waiter)
admin.site.register(Restaurant)
