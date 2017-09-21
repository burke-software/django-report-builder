django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![pipeline status](https://gitlab.com/burke-software/django-report-builder/badges/master/pipeline.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)
[![coverage report](https://gitlab.com/burke-software/django-report-builder/badges/master/coverage.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)

# News

## 4.0

- Removed python 2.7 support, please use 3.6 for python 2.
- Added scheduled reports

## 3.6

- Fix bug affecting Django 1.10 and 1.11
- Moved to tox for testing

# What is Django Report Builder?

![](docs/screenshots/reportbuilderscreen.png)

## Features

- Add filters
- Add display fields
- Preview and create xlsx reports
- Very simple security, user must have change or "view" permission to view
reports. Unprivileged users can still build reports and see database schema.
- Model properties (thanks yekibud)
- Export to Report global admin action
- Scheduled reports can generate and send to users on cron like schedule
- Optional asynchronous report generation

# Documentation

http://django-report-builder.readthedocs.org/

[Google group](https://groups.google.com/forum/#!forum/django-report-builder/).

[Hacking](http://django-report-builder.readthedocs.org/en/latest/hacking/)
