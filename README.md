# django-report-builder

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![pipeline status](https://gitlab.com/burke-software/django-report-builder/badges/master/pipeline.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)
[![coverage report](https://gitlab.com/burke-software/django-report-builder/badges/master/coverage.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)

# News

## 6.0

- Added django 2.0 support. Droped support for Django 1.8 and 1.10 as Django no longer supports them
- Bug fixes

## 5.0

* Complete rewrite of the frontend in Angular CLI
  * Removed the left sidebar, added a 'home' page
  * Other minor improvements and fixes
  * For anyone who has written a custom frontend: we made a few changes to the django template that you might need to look at. The API has remained the same - one additional route was added that returns information as JSON that was previously serialized in the django template.

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

[Hacking](http://django-report-builder.readthedocs.org/en/latest/hacking/)
