from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from report_builder.models import DisplayField, Report, FilterField, Format
from django.conf import settings


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
    
    
class StarredFilter(SimpleListFilter):
    title = 'Your starred reports'
    parameter_name = 'starred'
    def lookups(self, request, model_admin):
        return (
            ('Starred', 'Starred Reports'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'Starred':
            return queryset.filter(starred=request.user)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('ajax_starred', 'edit', 'name', 'description', 'root_model', 'created', 'modified', 'user_created', 'download_xlsx',)
    readonly_fields = ['slug']
    fields = ['name', 'description', 'root_model', 'slug']
    search_fields = ('name', 'description')
    list_filter = (StarredFilter, 'root_model', 'created', 'modified', 'user_created', 'user_modified')
    #inlines = [DisplayFieldInline, FilterFieldInline]
    list_display_links = []

    class Media:
        media_url = getattr(settings, 'STATIC_URL', '/media')
        js = [ media_url+'/report_builder/js/report_list.js', ]

    def response_add(self, request, obj, post_url_continue=None):
        if '_easy' in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(ReportAdmin, self).response_add(request, obj, post_url_continue)
    
    def response_change(self, request, obj):
        if '_easy' in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(ReportAdmin, self).response_change(request, obj)
        
    def edit(self, obj):
        return '<a href="%s">Edit</a>' % obj.get_absolute_url()
    edit.allow_tags = True
    
    def download_xlsx(self, obj):
        return '<a href="%s">Download</a>' % reverse('report_builder.views.download_xlsx', args=[obj.id])
    download_xlsx.allow_tags = True    
    download_xlsx.short_description = "Download"
    
    def ajax_starred(self, obj):
        return '<a href="javascript:void(0)" onclick="ajax_add_star(this, \'{0}\')">S</a>'.format(reverse('report_builder.views.ajax_add_star', args=[obj.id]))
    ajax_starred.allow_tags = True
    ajax_starred.short_description = "Starred"
    
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user_created = request.user
        obj.user_modified = request.user
        obj.save()
    
admin.site.register(Report, ReportAdmin)
admin.site.register(Format)
