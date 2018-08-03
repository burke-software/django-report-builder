# django-report-builder

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![pipeline status](https://gitlab.com/burke-software/django-report-builder/badges/master/pipeline.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)
[![coverage report](https://gitlab.com/burke-software/django-report-builder/badges/master/coverage.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)

# News

## 6.2 (work in progress)

- Added Python 3.7 support.

## 6.1

- Added Django 2.1 support. 2.0 and 1.11 are still supported.

## 6.0

- Added django 2.0 support. Dropped support for Django 1.8 and 1.10 as Django no longer supports them
- Bug fixes

# What is Django Report Builder?

![](docs/screenshots/reportbuilderscreen.jpg)

## Features

* Add filters
* Add display fields
* Preview and create xlsx reports
* Very simple security, user must have change or "view" permission to view
  reports. Unprivileged users can still build reports and see database schema.
* Model properties (thanks yekibud)
* Export to Report global admin action
* Scheduled reports can generate and send to users on cron like schedule
* Optional asynchronous report generation

# Documentation

http://django-report-builder.readthedocs.org/

[Google group](https://groups.google.com/forum/#!forum/django-report-builder/).

[Contributing](http://django-report-builder.readthedocs.org/en/latest/contributors/)
