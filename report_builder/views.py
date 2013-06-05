from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from report_builder.models import Report, DisplayField, FilterField, Format
from report_builder.utils import javascript_date_format, duplicate
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django import forms

import datetime
import time
import re
from decimal import Decimal
from numbers import Number
from types import BooleanType
import copy
from dateutil import parser


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'root_model']


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'description',]
        widgets = {
            'description': forms.TextInput(attrs={'style': 'width:99%;'}),
        }
    
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
        if 'DateField' in self.instance.field_verbose or 'DateTimeField' in self.instance.field_verbose:
            widget = self.fields['filter_value'].widget
            widget.attrs['class'] = 'datepicker'
            widget.attrs['data-date-format'] = javascript_date_format(settings.DATE_FORMAT)


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

def get_custom_fields_from_model(model_class):
    """ django-custom-fields support
    """
    if 'custom_field' in settings.INSTALLED_APPS:
        from custom_field.models import CustomField
        try:
            content_type = ContentType.objects.get(model=model_class._meta.module_name,app_label=model_class._meta.app_label)
        except ContentType.DoesNotExist:
            content_type = None
        custom_fields = CustomField.objects.filter(content_type=content_type)
        return custom_fields

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
    custom_fields = get_custom_fields_from_model(model)
    root_model = model.__name__.lower()

    if field_name == '':
        return render_to_response('report_builder/report_form_fields_li.html', {
            'fields': get_direct_fields_from_model(model),
            'properties': properties,
            'custom_fields': custom_fields,
            'root_model': root_model,
        }, RequestContext(request, {}),)
    
    field = model._meta.get_field_by_name(field_name)
    if path_verbose:
        path_verbose += "::"
    # TODO: need actual model name to generate choice list (not pluralized field name)
    # - maybe store this as a separate value?
    if field[3] and hasattr(field[0], 'm2m_reverse_field_name'):
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
    custom_fields = get_custom_fields_from_model(new_model)
    properties = get_properties_from_model(new_model)

    return render_to_response('report_builder/report_form_fields_li.html', {
        'fields': fields,
        'custom_fields': custom_fields,
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
    select_widget = forms.Select(choices=[('','---------')] + list(choices))
    options_html = select_widget.render_options([], [0])
    return HttpResponse(options_html)

def ajax_get_formats(request):
    choices = Format.objects.values_list('pk', 'name')
    select_widget = forms.Select(choices=[('','---------')] + list(choices))
    options_html = select_widget.render_options([], [0])
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


def sort_helper(x, sort_key):
    # TODO: explain what's going on here - I think this is meant to deal with
    # null comparisons for datetimes? 
    if x[sort_key] == None:
        result = datetime.date(datetime.MINYEAR, 1, 1)
    else:
        result = x[sort_key]     
    return result.lower() if isinstance(result, basestring) else result

def report_to_list(report, user, preview=False, queryset=None):
    """ Create list from a report with all data filtering
    preview: Return only first 50
    objects: Provide objects for list, instead of running filters
    Returns list, message in case of issues
    """
    message= ""
    model_class = report.root_model.model_class()
    if queryset != None:
        objects = report.add_aggregates(queryset)
    else:
        try:
            objects = report.get_query()
        except exceptions.ValidationError, e:
            message += "Validation Error: {0!s}. This probably means something is wrong with the report's filters.".format(e)
            return [], message

    # Display Values
    display_field_paths = []
    property_list = {}
    custom_list = {}
    display_totals = {}
    def append_display_total(display_totals, display_field, display_field_key):
        if display_field.total:
            display_totals[display_field_key] = {'val': Decimal('0.00')}


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
            elif '[custom' in display_field.field_verbose:
                custom_list[i] = display_field_key 
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

            def increment_total(display_field_key, display_totals, val):
                if display_totals.has_key(display_field_key):
                    # Booleans are Numbers - blah
                    if isinstance(val, Number) and not isinstance(val, BooleanType):
                        # do decimal math for all numbers
                        display_totals[display_field_key]['val'] += Decimal(str(val))
                    else:
                        display_totals[display_field_key]['val'] += Decimal('1.00')


            # get pk for primary and m2m relations in order to retrieve objects 
            # for adding properties to report rows
            display_field_paths.insert(0, 'pk')
            m2m_relations = []
            for position, property_path in property_list.iteritems():
                property_root = property_path.split('__')[0]
                root_class = report.root_model.model_class()
                property_root_class = getattr(root_class, property_root)
                if type(property_root_class) == ReverseManyRelatedObjectsDescriptor:
                    display_field_paths.insert(1, '%s__pk' % property_root)
                    m2m_relations.append(property_root)
            values_and_properties_list = []
            filtered_report_rows = []
            group = None 
            for df in report.displayfield_set.all():
                if df.group:
                    group = df.path + df.field
                    break
            if group:
                filtered_report_rows = report.add_aggregates(objects.values_list(group))
            else:
                values_list = objects.values_list(*display_field_paths)

            if not group: 
                for row in values_list:
                    row = list(row)
                    obj = report.root_model.model_class().objects.get(pk=row.pop(0)) 
                    #related_objects
                    remove_row = False
                    values_and_properties_list.append(row)
                    # filter properties (remove rows with excluded properties)
                    property_filters = report.filterfield_set.filter(
                        field_verbose__contains='[property]'
                        )
                    for property_filter in property_filters: 
                        root_relation = property_filter.path.split('__')[0]
                        if root_relation in m2m_relations: 
                            pk = row[0]
                            if pk is not None:
                                # a related object exists
                                m2m_obj = getattr(obj, root_relation).get(pk=pk)
                                val = reduce(getattr, [property_filter.field], m2m_obj)
                            else:
                                val = None
                        else:
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
                            relations = display_property.split('__')
                            root_relation = relations[0]
                            if root_relation in m2m_relations: 
                                pk = row.pop(0)
                                if pk is not None:
                                    # a related object exists
                                    m2m_obj = getattr(obj, root_relation).get(pk=pk)
                                    val = reduce(getattr, relations[1:], m2m_obj)
                                else:
                                    val = None
                            else:
                                val = reduce(getattr, relations, obj)
                            values_and_properties_list[-1].insert(position, val)
                            increment_total(display_property, display_totals, val)
                        for position, display_custom in custom_list.iteritems(): 
                            val = obj.get_custom_value(display_custom)
                            values_and_properties_list[-1].insert(position, val)
                            increment_total(display_custom, display_totals, val)
                        filtered_report_rows += [values_and_properties_list[-1]]
                    if preview and len(filtered_report_rows) == 50:
                        break
            sort_fields = report.displayfield_set.filter(sort__gt=0).order_by('-sort').\
                values_list('position', 'sort_reverse')
            for sort_field in sort_fields:
                filtered_report_rows = sorted(
                        filtered_report_rows,
                        key=lambda x: sort_helper(x, sort_field[0]-1),
                        reverse=sort_field[1]
                        )
            values_and_properties_list = filtered_report_rows
        else:
            values_and_properties_list = []
            message = "Permission Denied on %s" % report.root_model.name


        # add choice list display and display field formatting
        choice_lists = {} 
        display_formats = {} 
        final_list = []
        for df in report.displayfield_set.all():
            if df.choices:
                df_choices = df.choices_dict
                # Insert blank and None as valid choices
                df_choices[''] = ''
                df_choices[None] = ''
                choice_lists.update({df.position: df_choices}) 
            if df.display_format:
                display_formats.update({df.position: df.display_format}) 
        for row in values_and_properties_list:
            # add display totals for grouped result sets
            # TODO: dry this up, duplicated logic in non-grouped total routine 
            if group:
                # increment totals for fields
                for i, field in enumerate(display_field_paths[1:]):
                    if field in display_totals.keys():
                        increment_total(field, display_totals, row[i])
            row = list(row)
            for position, choice_list in choice_lists.iteritems():
                row[position-1] = choice_list[row[position-1]]
            for position, display_format in display_formats.iteritems():
                # convert value to be formatted into Decimal in order to apply
                # numeric formats
                try:
                    value = Decimal(row[position-1])
                except:
                    value = row[position-1]
                # Try to format the value, let it go without formatting for ValueErrors
                try:
                    row[position-1] = display_format.string.format(value)
                except ValueError:
                    row[position-1] = value
            final_list.append(row)
        values_and_properties_list = final_list


        if display_totals:
            display_totals_row = []
            
            fields_and_properties = list(display_field_paths[1:])
            for position, value in property_list.iteritems(): 
                fields_and_properties.insert(position, value)
            for i, field in enumerate(fields_and_properties): 
                if field in display_totals.keys():
                    display_totals_row += [display_totals[field]['val']]
                else:
                    display_totals_row += ['']

            # add formatting to display totals
            for df in report.displayfield_set.all():
                if df.display_format:
                    try:
                        value = Decimal(display_totals_row[df.position-1])
                    except:
                        value = display_totals_row[df.position-1]
                    display_totals_row[df.position-1] = df.display_format.string.\
                        format(value)

        if display_totals:
            values_and_properties_list = (
                values_and_properties_list + [
                    ['TOTALS'] + (len(fields_and_properties) - 1) * ['']
                    ] + [display_totals_row]
                )

                

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
        custom_fields = get_custom_fields_from_model(model_class)

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
        ctx['custom_fields'] = custom_fields
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
            self.object.check_report_display_field_positions()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
@staff_member_required
def download_xlsx(request, pk, queryset=None):
    """ Download the full report in xlsx format
    Why xlsx? Because there is no decent ods library for python and xls has limitations 
    queryset: predefined queryset to bypass filters
    """
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
    
    objects_list, message = report_to_list(report, request.user, queryset=queryset)
    for row in objects_list:
        try:
            ws.append(row)
        except ValueError as e:
            ws.append([e.message])
        except:
            ws.append(['Unknown Error'])
    
    myfile = StringIO.StringIO()
    myfile.write(save_virtual_workbook(wb))
    response = HttpResponse(
        myfile.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = myfile.tell()
    return response
    

@staff_member_required
def ajax_add_star(request, pk):
    """ Star or unstar report for user
    """
    report = get_object_or_404(Report, pk=pk)
    user = request.user
    if user in report.starred.all():
        added = False
        report.starred.remove(request.user)
    else:
        added = True
        report.starred.add(request.user)
    return HttpResponse(added)
    
@staff_member_required
def create_copy(request, pk):
    """ Copy a report including related fields """
    report = get_object_or_404(Report, pk=pk)
    new_report = duplicate(report, changes=(
        ('name', '{} (copy)'.format(report.name)),
        ('user_created', request.user),
        ('user_modified', request.user),
    ))
    # duplicate does not get related
    for display in report.displayfield_set.all():
        new_display = copy.copy(display)
        new_display.pk = None
        new_display.report = new_report
        new_display.save()
    for report_filter in report.filterfield_set.all():
        new_filter = copy.copy(report_filter)
        new_filter.pk = None
        new_filter.report = new_report
        new_filter.save()
    return redirect(new_report)


@staff_member_required
def export_to_report(request):
    """ Export objects (by ID and content type) to an existing or new report
    In effect this runs the report with it's display fields. It ignores 
    filters and filters instead the provided ID's. It can be select
    as a global admin action.
    """
    admin_url = request.GET.get('admin_url', '/')
    ct = ContentType.objects.get_for_id(request.GET['ct'])
    ids = request.GET['ids'].split(',')
    number_objects = len(ids)
    reports = Report.objects.filter(root_model=ct).order_by('-modified')
    
    if 'download' in request.GET:
        report = get_object_or_404(Report, pk=request.GET['download'])
        queryset = ct.model_class().objects.filter(pk__in=ids)
        return download_xlsx(request, report.id, queryset=queryset)
    
    return render(request, 'report_builder/export_to_report.html', {
        'object_list': reports,
        'admin_url': admin_url,
        'number_objects': number_objects,
        'model': ct.model_class()._meta.verbose_name,
        })
