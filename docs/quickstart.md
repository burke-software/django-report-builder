#Quick Start Guide

##Requirements

Supported versions:

We follow Django's supported version schedule for new releases. No longer supported versions should use previous versions of report builder.

- Django -  1.8, 1.10, and 1.11
- Django Rest Framework 3.4+ 
- Python - 3.5 and 3.6.

##Installation

1. `pip install django-report-builder`
2. Add `report_builder` to INSTALLED_APPS
3. Add `url(r'^report_builder/', include('report_builder.urls'))` to url.py url patterns
4. Ensure `django.core.context_processors.static` and `django.core.context_processors.media` are in `TEMPLATE_CONTEXT_PROCESSORS`
    * Note: For Django 1.8+ template context processors have been moved from `django.core.context_processors` to
      `django.template.context_processors`. The settings for template context processors have moved from
      `TEMPLATE_CONTEXT_PROCESSORS` to be part of the template engine specific configuration in `TEMPLATES`,
      [as described here](https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/#the-templates-settings).
5. Sync your database. `python manage.py migrate`
6. Use Django admin or navigate to /report_builder/
 
Django Rest Framework must have Session Authentication enabled. Note this is enabled by default.

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework.authentication.SessionAuthentication',
    )
}
```

### Scheduled Reports

If using celery - you can set up scheduled reports to be sent on a recurring basis.

1. Ensure 'django_celery_beat' is in INSTALLED_APPS
2. Add 'report_builder_scheduled' to INSTALLED_APPS
3. Schedule a celery periodic task to process the report builder scheduled tasks. `report_builder_scheduled.tasks.report_builder_check_if_scheduled_report`. Run it every 10 minutes or so. Note that this task will simply schedule other report generating tasks so it should be very short lived even if there are long reports that need to run.

##Settings

### Include and exclude fields and models

To include a model you've to specify the app your models belong to. If your 'user' model is in the app 'hr' then you can do the following to include it:

    REPORT_BUILDER_INCLUDE = ['hr.user'] # Allow only the model user to be accessed

The same reasoning also applies to exclude models. If your 'account' model is in the app 'finance' then you can do the following to exclude it:

    REPORT_BUILDER_EXCLUDE = ['finance.account'] # Allow all models except account to be accessed

### Per model settings

You may also limit which fields in a model can be used. Add this class and these properties to a model
This works similar to Django's Meta class.

    class ReportBuilder:
        exclude = ()  # Lists or tuple of excluded fields
        fields = ()   # Explicitly allowed fields
        extra = ()    # List extra fields (useful for methods)

Note you can add properties in a similar way as Django admin.

In previous versions of django-report-builder all properties were included by default.
They must now be explicitly included.

Moreover, we have added functionality to set fields to display by default. This is currently not valuable to the front-end that django-report-builder comes with, but if you have your own front-end then you could utilize this information. The aim is that when you select the model you want to filter on these fields would be selected as display defaults automatically.

    class ReportBuilder:
        defaults = () # Lists or tuple of defaults

The `defaults` field would usually be a subset of the `fields`. The idea is that you would have a `is_defualt` field on the JSON-frontend that would allow you to recognize that this is a default value on your own front-end.

You can also mark which fields you would like to set as filters for the JSON end-point. This is currently not valuable to the front-end that django-report-builder comes with, but if you have your own front-end then you could utilize this information.

This filter is purely cosmetic, and not used in any way internally in the configuration of report-builder. This is not a security measure.

    class ReportBuilder:
        filters = () # Lists or tuple of filters

The distinction here is only created if you want to differentiate display fields and filters. It is possible by this to create a distinction between a display field and a field the user can filter by.

### Custom model manager for all models

    REPORT_BUILDER_MODEL_MANAGER = 'on_site' #name of custom model manager to use on all models

You may also set a custom model manager per model. Just add the custom model manager and this property to a model

    report_builder_model_manager = on_site #reference to custom model manager to use for a model

### Export to Report

Admin action is disabled by default. To enable set
    
    REPORT_BUILDER_GLOBAL_EXPORT = True

This allows users to select lists of objects in django admin's change_list view and export them to a predefined report.
In effect bypasses the report's filters using the checked off objects instead.

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

### Email notification when file is uploaded

The reports are emailed to the current user rather than generated and then downloaded. This is if you have reports that take a while to generate or if you'd prefer your users to be emailed.

The current front-end simply downloads the report right away, and so this is a feature you'll have to enable on the front-end yourself (or the package will support it in the future).

    REPORT_BUILDER_EMAIL_NOTIFICATION = True

This uses the default django mail implementation. The code checks for either `EMAIL_BACKEND` or `EMAIL_HOST` to be defined in the `settings.py` file. You should also define `DEFAULT_FROM_EMAIL`.

You're also able to stylize the templates according to your needs. To enable the reports:

    REPORT_BUILDER_EMAIL_NOTIFICATION = True
    REPORT_BUILDER_EMAIL_SUBJECT = ""

This package uses Django-Templates for its email templates. The report path it uses is `email/email_report.html`, and you're able to overwrite this in your own django application.

The `{{report}}` element is what would be replaced with the report URL, and the `{{name}}`. The field `REPORT_BUILDER_EMAIL_SUBJECT` will be defaulted to 'Report is ready' if missing.

### Turn off front-end

If you're developing your own front-end then you would need the ability to disable the front-end that comes with this package. To disable the built-in front-end:

    REPORT_BUILDER_FRONTEND = False

By default the front-end is turned on.
