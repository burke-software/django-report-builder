from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Max, Min, Count
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from report_builder.models import Report, DisplayField, FilterField
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from django import forms

import datetime
from dateutil import parser

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'root_model']


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct',]
    
    
class DisplayFieldForm(forms.ModelForm):
    class Meta:
        model = DisplayField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
            'width': forms.TextInput(attrs={'class':'small_input'}),
            'sort': forms.TextInput(attrs={'class':'small_input'}),
        }
        

class FilterFieldForm(forms.ModelForm):
    class Meta:
        model = FilterField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
            'filter_type': forms.Select(attrs={'onchange':'check_filter_type(event.target)'})
        }


class ReportCreateView(CreateView):
    form_class = ReportForm
    template_name = 'report_new.html'
    

def get_relation_fields_from_model(model_class):
    relation_fields = []
    all_fields_names = model_class._meta.get_all_field_names()
    for field_name in all_fields_names:
        field = model_class._meta.get_field_by_name(field_name)
        if field[3] or not field[2] or hasattr(field[0], 'related'):
            field[0].field_name = field_name
            relation_fields += [field[0]]
    return relation_fields

def get_direct_fields_from_model(model_class):
    direct_fields = []
    all_fields_names = model_class._meta.get_all_field_names()
    for field_name in all_fields_names:
        field = model_class._meta.get_field_by_name(field_name)
        # Direct, not m2m, not FK
        if field[2] and not field[3] and field[0].__class__.__name__ != "ForeignKey":
            direct_fields += [field[0]]
    return direct_fields
            
def ajax_get_related(request):
    """ Get related model and fields
    Requires get variables model and field
    Returns the model the field belongs to
    """
    field_name = request.GET['field']
    model = ContentType.objects.get(pk=request.GET['model']).model_class()
    field = model._meta.get_field_by_name(field_name)
    path = request.GET['path']
    path_verbose = request.GET['path_verbose']
    
    if field[2]:
        # Direct field
        new_model = field[0].related.parent_model()
    else:
        # Indirect related field
        new_model = field[0].model()
    
    new_fields = get_relation_fields_from_model(new_model)
    model_ct = ContentType.objects.get_for_model(new_model)
    
    if path_verbose:
        path_verbose += "::"
    path_verbose += field[0].name
    
    path += field_name
    path += '__'
    
    return render_to_response('report_builder/report_form_related_li.html', {
        'model_ct': model_ct,
        'related_fields': new_fields,
        'path': path,
        'path_verbose': path_verbose,
    }, RequestContext(request, {}),)

def ajax_get_fields(request):
    """ Get fields for a particular model
    """
    field_name = request.GET['field']
    model = ContentType.objects.get(pk=request.GET['model']).model_class()
    path = request.GET['path']
    path_verbose = request.GET['path_verbose']
    
    if field_name == '':
        return render_to_response('report_builder/report_form_fields_li.html', {
            'fields': get_direct_fields_from_model(model),
        }, RequestContext(request, {}),)
    
    field = model._meta.get_field_by_name(field_name)
    if path_verbose:
        path_verbose += "::"
    path_verbose += field[0].name
    
    path += field_name
    path += '__'
    
    if field[2]:
        # Direct field
        new_model = field[0].related.parent_model()
    else:
        # Indirect related field
        new_model = field[0].model()
    
    fields = get_direct_fields_from_model(new_model)
    
    return render_to_response('report_builder/report_form_fields_li.html', {
        'fields': fields,
        'path': path,
        'path_verbose': path_verbose,
    }, RequestContext(request, {}),)

def get_model_from_path_string(root_model, path):
    """ Return a model class for a related model
    root_model is the class of the initial model
    path is like foo__bar where bar is related to foo
    """
    for path_section in path.split('__'):
        if path_section:
            field = root_model._meta.get_field_by_name(path_section)
            if field[2]:
                root_model = field[0].related.parent_model()
            else:
                root_model = field[0].model
    return root_model

def report_to_list(report, user, preview=False):
    """ Create list from a report with all data filtering
    Returns list, message in case of issues
    """
    message= ""
    
    model_class = report.root_model.model_class()
    
    objects = model_class.objects.all()
    
    # Filters
    for filter_field in report.filterfield_set.all():
        try:
            filter_string = str(filter_field.path + filter_field.field)
            
            if filter_field.filter_type:
                filter_string += '__' + filter_field.filter_type
            
            # Check for special types such as isnull
            if filter_field.filter_type == "isnull" and filter_field.filter_value == "0":
                filter_list = {filter_string: False}
            else:
                # All filter values are stored as strings, but may need to be converted
                if '[DateField]' in filter_field.field_verbose:
                    filter_value = parser.parse(filter_field.filter_value)
                else:
                    filter_value = filter_field.filter_value
                filter_list = {filter_string: filter_value}
                
            if not filter_field.exclude:
                objects = objects.filter(**filter_list)
            else:
                objects = objects.exclude(**filter_list)
        except:
            message += "Filter Error on %s. If you are using the report builder then " % filter_field.field_verbose
            message += "you found a bug! "
            message += "If you made this in admin, then you probably did something wrong."
    
    # Aggregates
    for display_field in report.displayfield_set.filter(aggregate__isnull=False):
        if display_field.aggregate == "Avg":
            objects = objects.annotate(Avg(display_field.path + display_field.field))
        elif display_field.aggregate == "Max":
            objects = objects.annotate(Max(display_field.path + display_field.field))
        elif display_field.aggregate == "Min":
            objects = objects.annotate(Min(display_field.path + display_field.field))
        elif display_field.aggregate == "Count":
            objects = objects.annotate(Count(display_field.path + display_field.field))
    
    # Ordering
    order_list = []
    for display_field in report.displayfield_set.filter(sort__isnull=False).order_by('sort'):
        if display_field.sort_reverse:
            order_list += ['-' + display_field.path + display_field.field]
        else:
            order_list += [display_field.path + display_field.field]
    objects = objects.order_by(*order_list)
    
    # Distinct
    if report.distinct:
        objects = objects.distinct()
    
    # Limit because this is a preview
    if preview:
        objects = objects[:50]
    
    # Display Values
    values_list = []
    for display_field in report.displayfield_set.all():
        model = get_model_from_path_string(model_class, display_field.path)
        if user.has_perm(model._meta.app_label + '.change_' + model._meta.module_name) \
        or user.has_perm(model._meta.app_label + '.view_' + model._meta.module_name) \
        or not model:
            if display_field.aggregate == "Avg":
                values_list += [display_field.path + display_field.field + '__ave']
            elif display_field.aggregate == "Max":
                values_list += [display_field.path + display_field.field + '__max']
            elif display_field.aggregate == "Min":
                values_list += [display_field.path + display_field.field + '__min']
            elif display_field.aggregate == "Count":
                values_list += [display_field.path + display_field.field + '__count']
            else:
                values_list += [display_field.path + display_field.field]
        else:
            message += "You don't have permission to " + display_field.name
    try:
        if user.has_perm(report.root_model.app_label + '.change_' + report.root_model.model) \
        or user.has_perm(report.root_model.app_label + '.view_' + report.root_model.model):
            objects_list = objects.values_list(*values_list)
        else:
            objects_list = []
            message = "Permission Denied on %s" % report.root_model.name
    except exceptions.FieldError:
        message += "Field Error. If you are using the report builder then you found a bug!"
        message += "If you made this in admin, then you probably did something wrong."
        objects_list = None
    
    return objects_list, message
    
@staff_member_required
def ajax_preview(request):
    """ This view is intended for a quick preview useful when debugging
    reports. It limits to 50 objects.
    """
    report = get_object_or_404(Report, pk=request.POST['report_id'])
    objects_list, message = report_to_list(report, request.user, preview=True)
    
    return render_to_response('report_builder/html_report.html', {
        'report': report,
        'objects_dict': objects_list,
        'message': message
        
    }, RequestContext(request, {}),)

class ReportUpdateView(UpdateView):
    """ This view handles the edit report builder
    It includes attached formsets for display and criteria fields
    """
    model = Report
    form_class = ReportEditForm
    success_url = './'
    
    @method_decorator(permission_required('report_builder.change_report'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReportUpdateView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super(ReportUpdateView, self).get_context_data(**kwargs)
        model_class = self.object.root_model.model_class()
        model_ct = ContentType.objects.get_for_model(model_class)
        
        direct_fields = get_direct_fields_from_model(model_class)
        relation_fields = get_relation_fields_from_model(model_class)
        
        DisplayFieldFormset = inlineformset_factory(
            Report,
            DisplayField,
            extra=0,
            can_delete=True,
            form=DisplayFieldForm)
        
        FilterFieldFormset = inlineformset_factory(
            Report,
            FilterField,
            extra=0,
            can_delete=True,
            form=FilterFieldForm)
        
        if self.request.POST:
            ctx['field_list_formset'] =  DisplayFieldFormset(self.request.POST, instance=self.object)
            ctx['field_filter_formset'] =  FilterFieldFormset(self.request.POST, instance=self.object, prefix="fil")
        else:
            ctx['field_list_formset'] =  DisplayFieldFormset(instance=self.object)
            ctx['field_filter_formset'] =  FilterFieldFormset(instance=self.object, prefix="fil")
        
        ctx['related_fields'] = relation_fields
        ctx['fields'] = direct_fields
        ctx['model_ct'] = model_ct
        
        return ctx
    
    def form_valid(self, form):
        context = self.get_context_data()
        field_list_formset = context['field_list_formset']
        field_filter_formset = context['field_filter_formset']
        
        if field_list_formset.is_valid() and field_filter_formset.is_valid():
            self.object = form.save()
            field_list_formset.report = self.object
            field_list_formset.save()
            field_filter_formset.report = self.object
            field_filter_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
@staff_member_required
def download_xlsx(request, pk):
    """ Download the full report in xlsx format
    Why xlsx? Because there is no decent ods library for python and xls has limitations """
    import cStringIO as StringIO
    from openpyxl.workbook import Workbook
    from openpyxl.writer.excel import save_virtual_workbook
    from openpyxl.cell import get_column_letter
    import re

    report = get_object_or_404(Report, pk=pk)
    
    wb = Workbook()
    ws = wb.worksheets[0]
    ws.title = report.name
    filename = re.sub(r'\W+', '', report.name) + '.xlsx'
    
    i = 0
    for field in report.displayfield_set.all():
        cell = ws.cell(row=0, column=i)
        cell.value = field.name
        cell.style.font.bold = True
        ws.column_dimensions[get_column_letter(i+1)].width = field.width
        i += 1
    
    objects_list, message = report_to_list(report, request.user)
    for row in objects_list:
        ws.append(row)
    
    myfile = StringIO.StringIO()
    myfile.write(save_virtual_workbook(wb))
    response = HttpResponse(
        myfile.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = myfile.tell()
    return response
    
    
    