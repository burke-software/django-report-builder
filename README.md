django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might 
not be able to program or gain direct interactive shell access.


![](https://raw.github.com/burke-software/django-report-builder/master/screenshots/report.png)

What's finished?
- Add filters
- Add display fields
- Preview and create xlsx reports

What isn't
- Security!
- More exports, views
- Decent form validation
- Functions in display fields
- Support for django-custom-fields

# Installation

1. pip install django-report-builder openpyxl
1. Add report_builder to INSTALLED_APPS
1. Add url(r'^report_builder/', include('report_builder.urls')) to url.py url patterns
1. syncdb (you may use south)
1. Use admin access

Optional - limit which models can be used by adding in settings.py

REPORT_BUILDER_INCLUDE = []
REPORT_BUILDER_EXCLUDE = []

# Usage

Go to the admin site (/admin/report_builder) and create a report. You can use the "easy edit" button after saving
to get the screen in the screenshot. Select related fields in the top left section. Drag actual fields in the bottom
left section into either the filter or display tabs. Preview the report and when satified generate an xlsx file for the
full report.
