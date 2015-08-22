from django.contrib import admin
from custom_field.custom_field import CustomFieldAdmin
from .models import (
    Foo, Bar, Place, Waiter, Restaurant, Account, Person, Child
)


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    pass


@admin.register(Bar)
class BarAdmin(CustomFieldAdmin, admin.ModelAdmin):
    pass


admin.site.register(Account)
admin.site.register(Place)
admin.site.register(Waiter)
admin.site.register(Restaurant)
admin.site.register(Person)
admin.site.register(Child)
