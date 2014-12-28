django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. 
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder) [![Bountysource](https://www.bountysource.com/badge/tracker?tracker_id=314767)](https://www.bountysource.com/trackers/314767-burke-software-django-report-builder?utm_source=314767&utm_medium=shield&utm_campaign=TRACKER_BADGE)

[Support development on gittip](www.gittip.com/bufke)

# News

The master branch now has merged a totally redesigned frontend. This will be released as 3.0. 
For the old see the 2.x branch.

## 3.0 Changes

- Frontend redone in angular and material design.
- Async report status
- Requires Django 1.7 and Django Rest Framework 3.0. Users of older versions should continue to use the 2.x branch instead. I will continue to accept pull requests for 2.x however new features will be added only in 3.x.
- Responsive - Even works on mobile.
- API built with DRF - in theory you could impliment your own frontend.

# What is Django Report Builder?

![](https://raw.github.com/burke-software/django-report-builder/master/screenshots/reportbuilderscreen.png)

What's finished?
- Add filters
- Add display fields
- Preview and create xlsx reports
- Very simple security, user must have change or "view" permission to view 
reports. Unprivileged users can still build reports and see database schema.
- Model properties (thanks yekibud)
- Support for [django-custom-fields](https://github.com/burke-software/django-custom-field)
- Support for django-hstore
- Export to Report global admin action
- Optional asynchronous report generation

What isn't
- "or" filters together
- More exports, views
- Decent form validation

# Documentation

http://django-report-builder.readthedocs.org/

# Discussion

Let us know your thoughts at https://google.com/+Burkesoftware or consider sending some pull requests our way!
