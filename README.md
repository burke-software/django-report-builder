django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might not be able to program.

What's finished?
- Add filters
- Add display fields
- Preview and create xlsx reports

What isn't
- Security!
- Choosing which models are allowed or excluded
- More exports, views

# Installation
What? Well if you like unfinished stuff...

1. pip install django-report-builder openpyxl
1. Add report_builder to INSTALLED_APPS
1. Add url(r'^report_builder/', include('report_builder.urls')) to url.py url patterns
1. syncdb (you may use south)
1. Use admin access