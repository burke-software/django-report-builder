django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![pipeline status](https://gitlab.com/burke-software/django-report-builder/badges/master/pipeline.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)
[![coverage report](https://gitlab.com/burke-software/django-report-builder/badges/master/coverage.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)

# News

## 3.6 (WIP)

- Fix bug affecting Django 1.10 and 1.11
- Moved to tox for testing

## 3.5

- Compatible with Django 1.11
- Manifest containers only needed static assets, greatly reducing file size.
- No longer testing in Django 1.9, but probably still works.
- Remains in maintence mode - no features

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
- Optional asynchronous report generation

# Documentation

http://django-report-builder.readthedocs.org/

[Google group](https://groups.google.com/forum/#!forum/django-report-builder/).

[Hacking](http://django-report-builder.readthedocs.org/en/latest/hacking/)
