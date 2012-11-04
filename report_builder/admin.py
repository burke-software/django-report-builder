from django.contrib import admin
from django import forms
from report_builder.models import DisplayField, Report


class DisplayFieldForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = DisplayField

class DisplayFieldInline(admin.TabularInline):
    model = DisplayField
    form = DisplayFieldForm
    extra = 0
    sortable_field_name = "position"
    
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'root_model', 'created', 'modified')
    inlines = [DisplayFieldInline]
    
admin.site.register(Report, ReportAdmin)