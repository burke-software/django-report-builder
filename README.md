django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might not be able to program.

Not finished yet, come back later!

# Installation
What? Well if you like unfinished stuff...
1. git clone and copy somewhere on python path. pypi support will come when it's finished.
1. Add report_builder to INSTALLED_APPS
1. Add url(r'^report_builder/', include('report_builder.urls')) to url.py url patterns
1. syncdb
1. Use admin access or go to /report_builder/report/add