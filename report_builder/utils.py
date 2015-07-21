from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
import copy


def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'Y', 'yyyy')
    format = format.replace(r'm', 'mm')
    format = format.replace(r'd', 'dd')
    if not format:
        format = 'yyyy-mm-dd'
    return format


def staff_member_required(view_func=None,
                          redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='admin:login'):
    if (not hasattr(settings, 'REPORT_BUILDER_STAFF_REQUIRED') or
            settings.REPORT_BUILDER_STAFF_REQUIRED):
        actual_decorator = user_passes_test(
            lambda u: u.is_active and u.is_staff,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: u.is_active,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


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
