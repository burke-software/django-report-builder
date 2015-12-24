from django.contrib import admin
from .models import Bar


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    pass
