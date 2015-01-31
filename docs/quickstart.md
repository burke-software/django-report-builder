#Quick Start Guide

##Installation

1. `pip install django-report-builder`
2. Add `report_builder` to INSTALLED_APPS
3. Add `url(r'^report_builder/', include('report_builder.urls'))` to url.py url patterns
4. Sync your database. `python manage.py migrate` 
5. Use Django admin or navigate to /report_builder/

##Settings

### Include and exclude fields and models

    REPORT_BUILDER_INCLUDE = []
    REPORT_BUILDER_EXCLUDE = ['user'] # Allow all models except User to be accessed

### Per model settings

You may also limit which fields in a model can be used. Add this class and these properties to a model
This works similar to Django's Meta class.

    class ReportBuilder:
        exclude = ()  # Lists or tuple of excluded fields
        fields = ()   # Explicitely allowed fields
        extra = ()    # List extra fields (useful for methods)

Note you can add properties in a similair way as Django admin.

In previous versions of django-report-builder all properties were included by default.
They must now be explicitly included.

### Custom model manager for all models

    REPORT_BUILDER_MODEL_MANAGER = 'on_site' #name of custom model manager to use on all models

You many also set a custom model manager per model. Just add the custom model manager and this property to a model

    report_builder_model_manager = on_site #reference to custom model manager to use for a model

### Export to Report

Admin action is disabled by default. To enable set
    
    REPORT_BUILDER_GLOBAL_EXPORT = True

### Asynchronous Report Generation

Sometimes it's useful to generate long running reports with a background worker. Defaults to off.
Advantages of this option

- Works better with Heroku which limits requests to 30 seconds
- Run a report, close your browser, come back later to a finished report
- Download the last report that was run instead of regenerating
- Nicer status messages about report status

**Installation**

1. Set up Celery
2. Set `REPORT_BUILDER_ASYNC_REPORT = True` in settings.py
