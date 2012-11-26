from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from report_builder.models import DisplayField, Report, FilterField


class DisplayFieldForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = DisplayField

class DisplayFieldInline(admin.StackedInline):
    model = DisplayField
    form = DisplayFieldForm
    extra = 0
    sortable_field_name = "position"

class FilterFieldForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = FilterField

class FilterFieldInline(admin.StackedInline):
    model = FilterField
    form = FilterFieldForm
    extra = 0
    sortable_field_name = "position"
    
class ReportAdmin(admin.ModelAdmin):
    list_display = ('easy_edit', 'admin_edit', 'name', 'download_xlsx', 'root_model', 'created', 'modified')
    inlines = [DisplayFieldInline, FilterFieldInline]
    list_display_links = ['admin_edit']
    
    def easy_edit(self, obj):
        return '<a href="%s">Edit</a>' % obj.get_absolute_url()
    easy_edit.allow_tags = True
    def admin_edit(self, obj):
        return 'Admin Edit'
    def download_xlsx(self, obj):
        return '<a href="%s">Download</a>' % reverse('report_builder.views.download_xlsx', args=[obj.id])
    download_xlsx.allow_tags = True
    
admin.site.register(Report, ReportAdmin)
