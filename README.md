django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder) [![Bountysource](https://www.bountysource.com/badge/tracker?tracker_id=314767)](https://www.bountysource.com/trackers/314767-burke-software-django-report-builder?utm_source=314767&utm_medium=shield&utm_campaign=TRACKER_BADGE)
[![Coverage Status](https://coveralls.io/repos/burke-software/django-report-builder/badge.svg)](https://coveralls.io/r/burke-software/django-report-builder)

# News

## 3.4

- Switched from default angular theme to something more neutral
- Updated Angular Material version
- Some CSS fixes
- Limited Django 1.10 (use >=3.4.2) support see #239
- Django rest framework 3.4 support


## 3.3 

Official support is now for Django 1.8 and 1.9. Python 2.7 and 3.5 (I'm sure 3.4 works but no longer unit testing it). For Django < 1.8 please use the 3.2 release.

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
