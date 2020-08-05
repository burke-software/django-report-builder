from decimal import Decimal
from itertools import chain
from numbers import Number
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
import copy
import datetime
import inspect


def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'Y', 'yyyy')
    format = format.replace(r'm', 'mm')
    format = format.replace(r'd', 'dd')
    if not format:
        format = 'yyyy-mm-dd'
    return format


def duplicate(obj, changes=None):
    """ Duplicates any object including m2m fields
    changes: any changes that should occur, example
    changes = (('fullname','name (copy)'), ('do not copy me', ''))"""
    if not obj.pk:
        raise ValueError('Instance must be saved before it can be cloned.')
    duplicate = copy.copy(obj)
    duplicate.pk = None
    for change in changes:
        duplicate.__setattr__(change[0], change[1])
    duplicate.save()
    # trick to copy ManyToMany relations.
    for field in obj._meta.many_to_many:
        source = getattr(obj, field.attname)
        destination = getattr(duplicate, field.attname)
        for item in source.all():
            try:  # m2m, through fields will fail.
                destination.add(item)
            except:
                pass
    return duplicate


DATE = 1
NUMBER = 2


def sort_helper(x, sort_key, sort_type):
    """ Sadly python 3 makes it very hard to sort mixed types
        We can work around this by forcing the types
    """
    result = x[sort_key]
    if result is None:
        if sort_type == DATE:
            result = datetime.date(datetime.MINYEAR, 1, 1)
        elif sort_type == NUMBER:
            result = 0
        else:  # Last try - make it a string
            result = ''
    return result


def sort_data(data_list, display_field):
    """ Sort data based on display_field settings
    data_list - 2d array of data
    display_field - report_builder.DisplayField object
    returns sorted data_list
    """
    position = display_field.position
    is_reverse = display_field.sort_reverse
    # Try to inspect sample data to determine type
    sample_data = data_list[0][position]
    if sample_data is None:
        sample_data = data_list[-1][position]
    sort_type = None
    if isinstance(sample_data, (datetime.date, datetime.datetime)):
        sort_type = DATE
    elif isinstance(sample_data, (int, float, complex)):
        sort_type = NUMBER
    return sorted(
        data_list,
        key=lambda x: sort_helper(x, position, sort_type),
        reverse=is_reverse
    )


def increment_total(display_field, data_row):
    val = data_row[display_field.position]
    if isinstance(val, bool):
        # True: 1, False: 0
        display_field.total_count += Decimal(val)
    elif isinstance(val, Number):
        display_field.total_count += Decimal(str(val))
    elif val:
        display_field.total_count += Decimal(1)


def formatter(value, style):
    """ Convert value to Decimal to apply numeric formats.
    value - The value we wish to format.
    style - report_builder.Format object
    """
    try:
        value = Decimal(value)
    except Exception:
        pass

    try:
        return style.string.format(value)
    except ValueError:
        return value


# Model Utils


def isprop(v):
    return isinstance(v, property)


def get_properties_from_model(model_class):
    """ Show properties from a model """
    properties = []
    attr_names = [name for (name, value) in inspect.getmembers(model_class, isprop)]
    for attr_name in attr_names:
        if attr_name.endswith('pk'):
            attr_names.remove(attr_name)
        else:
            properties.append(dict(label=attr_name, name=attr_name.strip('_').replace('_', ' ')))
    return sorted(properties, key=lambda k: k['label'])


def get_relation_fields_from_model(model_class):
    """ get related fields (m2m, fk, and reverse fk) """
    relation_fields = []
    all_fields_names = get_all_field_names(model_class)
    for field_name in all_fields_names:
        field = copy.deepcopy(model_class._meta.get_field(field_name))
        direct = field.concrete
        m2m = field.many_to_many
        # get_all_field_names will return the same field
        # both with and without _id. ignore the duplicate.
        if field_name[-3:] == '_id' and field_name[:-3] in all_fields_names:
            continue
        if m2m or not direct or field.is_relation:
            field.field_name = field_name
            relation_fields += [field]
    return relation_fields


def get_all_field_names(model_class):
    """ Restores a function from django<1.10 """
    return list(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in model_class._meta.get_fields()
        # For complete backwards compatibility, you may want to exclude
        # GenericForeignKey from the results.
        if not (field.many_to_one and field.related_model is None)
    )))


def get_direct_fields_from_model(model_class):
    """ Direct, not m2m, not FK """
    direct_fields = []
    all_fields_names = get_all_field_names(model_class)
    for field_name in all_fields_names:
        field = model_class._meta.get_field(field_name)
        direct = field.concrete
        m2m = field.many_to_many
        if direct and not m2m and not field.is_relation:
            direct_fields += [field]
    return direct_fields


def get_custom_fields_from_model(model_class):
    """ django-custom-fields support """
    if 'custom_field' in settings.INSTALLED_APPS:
        from custom_field.models import CustomField
        try:
            content_type = ContentType.objects.get(
                model=model_class._meta.model_name,
                app_label=model_class._meta.app_label)
        except ContentType.DoesNotExist:
            content_type = None
        custom_fields = CustomField.objects.filter(content_type=content_type)
        return custom_fields


def get_model_from_path_string(root_model, path):
    """ Return a model class for a related model
    root_model is the class of the initial model
    path is like foo__bar where bar is related to foo
    """
    for path_section in path.split('__'):
        if path_section:
            try:
                field = root_model._meta.get_field(path_section)
                direct = field.concrete
            except FieldDoesNotExist:
                return root_model
            if direct:
                if hasattr(field, 'related'):
                    try:
                        root_model = field.related.parent_model()
                    except AttributeError:
                        root_model = field.related.model

                elif hasattr(field, 'related_model') and field.related_model:
                    root_model = field.related_model

            else:
                if hasattr(field, 'related_model'):
                    root_model = field.related_model
                else:
                    root_model = field.model
    return root_model
