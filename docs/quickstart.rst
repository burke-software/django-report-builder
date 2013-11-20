.. _quickstart:

Quick Start Guide
=================

Installation
------------

1. ``pip install django-report-builder``
2. Add ``report_builder`` to INSTALLED_APPS
3. Add ``url(r'^report_builder/', include('report_builder.urls'))`` to url.py url patterns
4. Sync your database, we don't recommend running migrations on the initial install. 

    ./manage.py syncdb --all
    
    ./manage.py migrate --fake report_builder
    
5. Use Django admin to start building reports.

Settings
--------

You may include and exclude fields or entire models.

    REPORT_BUILDER_INCLUDE = []
    
    REPORT_BUILDER_EXCLUDE = ['user'] # Allow all models except User to be accessed

You may also limit which fields in a model can be used. Just add the property:

    report_builder_exclude_fields = () # Lists or tuple of excluded fields
    
Export to Report action is disabled by default. To enable set
    
    REPORT_BUILDER_GLOBAL_EXPORT = True
    
Fieldsets
---------

It's possible to group fields together in fieldsets. This might be useful if you have many fields in a model.
It follows syntax like Django Admin `fieldsets`__

__ https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) 

Add ``report_builder_fieldsets`` to your model in models.py. Classes are optional. Right now the only functional
class is 'collapse' which will hide the fields until clicked on.

Example:

::
    report_builder_fieldsets = (
        ('Names', {
            'fields': ('first_name', 'last_name'),
        }),
        ('More', {
            'fields': ('id', 'city'),
            'classes': ('collapse',),
        }),
    )
