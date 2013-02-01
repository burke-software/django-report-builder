from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Max, Min, Count, Sum, CharField
from django.db.models.manager import Manager
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
import time
import re
from operator import itemgetter
from decimal import Decimal
from numbers import Number
from types import BooleanType

from dateutil import parser


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'root_model', 'slug']


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct']
    
    
class DisplayFieldForm(forms.ModelForm):
    class Meta:
        model = DisplayField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
            'width': forms.TextInput(attrs={'class':'small_input'}),
            'total': forms.CheckboxInput(attrs={'class':'small_input'}),
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

    def __init__(self, *args, **kwargs):
        super(FilterFieldForm, self).__init__(*args, **kwargs)
        # override the filter_value field with the models native ChoiceField
        if self.instance.choices:
            self.fields['filter_value'].widget = forms.Select(choices=self.instance.choices)


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

def get_properties_from_model(model_class):
    properties = []
    for attr_name, attr in dict(model_class.__dict__).iteritems():
        if type(attr) == property:
            properties.append(dict(label=attr_name, name=attr_name.strip('_').replace('_',' ')))
    return sorted(properties)

def filter_property(filter_field, value):
    filter_type = filter_field.filter_type
    filter_value = filter_field.filter_value
    filtered = True 
    #TODO: i10n
    WEEKDAY_INTS = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }
    #TODO instead of catch all, deal with all cases
    # Example is 'a' < 2 is a valid python comparison
    # But what about 2 < '1' which yeilds true! Not intuitive for humans.
    try:
        if filter_type == 'exact' and str(value) == filter_value:
            filtered = False
        if filter_type == 'iexact' and str(value).lower() == str(filter_value).lower():
            filtered = False
        if filter_type == 'contains' and filter_value in value:
            filtered = False
        if filter_type == 'icontains' and str(filter_value).lower() in str(value).lower():
            filtered = False
        if filter_type == 'in' and value in filter_value:
            filtered = False
        # convert dates and datetimes to timestamps in order to compare digits and date/times the same
        if isinstance(value, datetime.datetime) or isinstance(value, datetime.date): 
            value = str(time.mktime(value.timetuple())) 
            try:
                filter_value_dt = parser.parse(filter_value)
                filter_value = str(time.mktime(filter_value_dt.timetuple()))
            except ValueError:
                pass
        if filter_type == 'gt' and Decimal(value) > Decimal(filter_value):
            filtered = False
        if filter_type == 'gte' and Decimal(value) >= Decimal(filter_value):
            filtered = False
        if filter_type == 'lt' and Decimal(value) < Decimal(filter_value):
            filtered = False
        if filter_type == 'lte' and Decimal(value) <= Decimal(filter_value):
            filtered = False
        if filter_type == 'startswith' and str(value).startswith(str(filter_value)):
            filtered = False
        if filter_type == 'istartswith' and str(value).lower().startswith(str(filter_value)):
            filtered = False
        if filter_type == 'endswith' and str(value).endswith(str(filter_value)):
            filtered = False
        if filter_type == 'iendswith' and str(value).lower().endswith(str(filter_value)):
            filtered = False
        if filter_type == 'range' and value in [int(x) for x in filter_value]:
            filtered = False
        if filter_type == 'week_day' and WEEKDAY_INTS.get(str(filter_value).lower()) == value.weekday:
            filtered = False
        if filter_type == 'isnull' and value == None:
            filtered = False
        if filter_type == 'regex' and re.search(filter_value, value):
            filtered = False
        if filter_type == 'iregex' and re.search(filter_value, value, re.I):
            filtered = False
    except:
        pass

    if filter_field.exclude:
        return not filtered
    return filtered 

            
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
    """ Get fields and properties for a particular model
    """
    field_name = request.GET.get('field')
    model = ContentType.objects.get(pk=request.GET['model']).model_class()
    path = request.GET['path']
    path_verbose = request.GET.get('path_verbose')
    properties = get_properties_from_model(model)
    root_model = model.__name__.lower()

    if field_name == '':
        return render_to_response('report_builder/report_form_fields_li.html', {
            'fields': get_direct_fields_from_model(model),
            'properties': properties,
            'root_model': root_model,
        }, RequestContext(request, {}),)
    
    field = model._meta.get_field_by_name(field_name)
    if path_verbose:
        path_verbose += "::"
    # TODO: need actual model name to generate choice list (not pluralized field name)
    # - maybe store this as a separate value?
    if field[3]:
        path_verbose += field[0].m2m_reverse_field_name()
    else:
        path_verbose += field[0].name
    
    path += field_name
    path += '__' 
    if field[2]:
        # Direct field
        new_model = field[0].related.parent_model
        path_verbose = new_model.__name__.lower()
    else:
        # Indirect related field
        new_model = field[0].model
        path_verbose = new_model.__name__.lower()
   
    fields = get_direct_fields_from_model(new_model)
    properties = get_properties_from_model(new_model)
    
    return render_to_response('report_builder/report_form_fields_li.html', {
        'fields': fields,
        'properties': properties,
        'path': path,
        'path_verbose': path_verbose,
        'root_model': root_model,
    }, RequestContext(request, {}),)

def ajax_get_choices(request):
    path_verbose = request.GET.get('path_verbose')
    label = request.GET.get('label')
    root_model = request.GET.get('root_model')
    choices = FilterField().get_choices(path_verbose or root_model, label)
    select_widget = forms.Select(choices=choices)
    options_html = select_widget.render_options(select_widget.choices, [0])
    return HttpResponse(options_html)

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
    objects = report.get_query()

    # Display Values
    display_field_paths = []
    property_list = {} 
    display_totals = {}
    def append_display_total(display_totals, display_field, display_field_key):
        if display_field.total:
            display_totals[display_field_key] = {'label': display_field.name, 'val': Decimal('0.00')}
        
    for i, display_field in enumerate(report.displayfield_set.all()):
        model = get_model_from_path_string(model_class, display_field.path)
        if user.has_perm(model._meta.app_label + '.change_' + model._meta.module_name) \
        or user.has_perm(model._meta.app_label + '.view_' + model._meta.module_name) \
        or not model:
            # TODO: clean this up a bit
            display_field_key = display_field.path + display_field.field
            if '[property]' in display_field.field_verbose:
                property_list[i] = display_field_key 
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Avg":
                display_field_key += '__avg'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Max":
                display_field_key += '__max'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Min":
                display_field_key += '__min'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Count":
                display_field_key += '__count'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Sum":
                display_field_key += '__sum'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            else:
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
        else:
            message += "You don't have permission to " + display_field.name
    try:
        if user.has_perm(report.root_model.app_label + '.change_' + report.root_model.model) \
        or user.has_perm(report.root_model.app_label + '.view_' + report.root_model.model):

            property_filters = {} 
            for property_filter in report.filterfield_set.filter(field_verbose__contains='[property]'):
                property_filters[property_filter.field] = property_filter 

            def increment_total(display_field_key, display_totals, val):
                if display_totals.has_key(display_field_key):
                    # Booleans are Numbers - blah
                    if isinstance(val, Number) and not isinstance(val, BooleanType):
                        # do decimal math for all numbers
                        display_totals[display_field_key]['val'] += Decimal(str(val))
                    else:
                        display_totals[display_field_key]['val'] += Decimal('1.00')

            # get pk in order to retrieve object for adding properties to report rows
            display_field_paths.insert(0, 'pk')
            values_and_properties_list = []
            filtered_report_rows = []
            group = None 
            for df in report.displayfield_set.all():
                if df.group:
                    group = df.field
                    break
            if group:
                filtered_report_rows = report.add_aggregates(objects.values_list(group))
            else:
                values_list = objects.values_list(*display_field_paths)

            if not group: 
                for row in values_list:
                    row = list(row)
                    obj = report.root_model.model_class().objects.get(pk=row.pop(0)) 
                    remove_row = False
                    values_and_properties_list.append(row)
                    # filter properties (remove rows with excluded properties)
                    for property_filter_label, property_filter in property_filters.iteritems():
                        val = reduce(getattr, (property_filter.path + property_filter.field).split('__'), obj)
                        if filter_property(property_filter, val):
                            remove_row = True
                            values_and_properties_list.pop()
                            break
                    if not remove_row:
                        # increment totals for fields
                        for i, field in enumerate(display_field_paths[1:]):
                            if field in display_totals.keys():
                                increment_total(field, display_totals, row[i])
                        for position, display_property in property_list.iteritems(): 
                            val = reduce(getattr, display_property.split('__'), obj)
                            values_and_properties_list[-1].insert(position, val)
                            increment_total(display_property, display_totals, val)
                        filtered_report_rows += [values_and_properties_list[-1]]
                    if preview and len(filtered_report_rows) == 50:
                        break
                if display_totals:
                    display_totals_row = ['TOTALS'] + [
                        '%s: %s' % (
                            display_totals[t]['label'],
                            display_totals[t]['val']
                        ) for t in display_totals
                    ]
            sort_fields = report.displayfield_set.filter(sort__gt=0).order_by('sort').\
                values_list('position', flat=True)
            if sort_fields:
                get_key = itemgetter(*[s-1 for s in sort_fields])
                values_and_properties_list = sorted(
                    filtered_report_rows,
                    key=lambda x: get_key(x).lower() if isinstance(get_key(x), basestring) else get_key(x)
                )
            if display_totals:
                values_and_properties_list = values_and_properties_list + [display_totals_row]
        else:
            values_and_properties_list = []
            message = "Permission Denied on %s" % report.root_model.name

        # add choice list display
        choice_lists = {} 
        final_list = []
        for df in report.displayfield_set.all():
            if df.choices:
                df_choices = df.choices_dict
                # Insert blank and None as valid choices
                df_choices[''] = ''
                df_choices[None] = ''
                choice_lists.update({df.position: df_choices}) 
        if choice_lists:
            for row in values_and_properties_list:
                row = list(row)
                for position, choice_list in choice_lists.iteritems():
                    row[position-1] = choice_list[row[position-1]]
                    final_list.append(row)
            values_and_properties_list = final_list
                

    except exceptions.FieldError:
        message += "Field Error. If you are using the report builder then you found a bug!"
        message += "If you made this in admin, then you probably did something wrong."
        values_and_properties_list = None

    return values_and_properties_list, message
    
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
        properties = get_properties_from_model(model_class)

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
        ctx['properties'] = properties
        ctx['model_ct'] = model_ct
        ctx['root_model'] = model_ct.model
        
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
    
    
    
