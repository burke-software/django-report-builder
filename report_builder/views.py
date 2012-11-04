from django.contrib.contenttypes.models import ContentType
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from report_builder.models import Report, DisplayField
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from django import forms

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'root_model']


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name',]
    
    
class DisplayFieldForm(forms.ModelForm):
    class Meta:
        model = DisplayField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
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
    print relation_fields
    return relation_fields

def get_direct_fields_from_model(model_class):
    direct_fields = []
    all_fields_names = model_class._meta.get_all_field_names()
    for field_name in all_fields_names:
        field = model_class._meta.get_field_by_name(field_name)
        if field[2]:
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

def ajax_preview(request):
    report = get_object_or_404(Report, pk=request.POST['report_id'])
    
    model_class = report.root_model.model_class()
    
    objects = model_class.objects.all()
    
    values_list = []
    for display_field in report.displayfield_set.all():
        values_list += [display_field.path + display_field.field]
    objects_dict = objects.values_list(*values_list)
    
    return render_to_response('report_builder/html_report.html', {
        'report': report,
        'objects_dict': objects_dict,
        
    }, RequestContext(request, {}),)
    
class ReportUpdateView(UpdateView):
    """ This view handles the edit report builder
    It includes attached formsets for display and criteria fields
    """
    model = Report
    form_class = ReportEditForm
    success_url = './'
    
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
        
        if self.request.POST:
            ctx['field_list_formset'] =  DisplayFieldFormset(self.request.POST, instance=self.object)
        else:
            ctx['field_list_formset'] =  DisplayFieldFormset(instance=self.object)
        
        ctx['related_fields'] = relation_fields
        ctx['fields'] = direct_fields
        ctx['model_ct'] = model_ct
        
        return ctx
    
    def form_valid(self, form):
        context = self.get_context_data()
        field_list_formset = context['field_list_formset']
        print field_list_formset
        if field_list_formset.is_valid():
            self.object = form.save()
            field_list_formset.report = self.object
            field_list_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))