django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might 
not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder) [![Bountysource](https://www.bountysource.com/badge/tracker?tracker_id=314767)](https://www.bountysource.com/trackers/314767-burke-software-django-report-builder?utm_source=314767&utm_medium=shield&utm_campaign=TRACKER_BADGE)

[Support development on gittip](www.gittip.com/bufke)

# News

Welcome to the 2.X branch. This is no longer the latest version but is maintained for compatbility with django <1.7, django rest framework<3.0 and those who wish to keep using the older django template interface.

# What is Django Report Builder?

![](/screenshots/reportbuilderscreen.png)

What's finished?
- Add filters
- Add display fields
- Preview and create xlsx reports
- Very simple security, user must have change or "view" permission to view 
reports. Unprivileged users can still build reports and see database schema.
- Model properties (thanks yekibud)
- Support for [django-custom-fields](https://github.com/burke-software/django-custom-field)
- Export to Report global admin action
- Optional asynchronous report generation

What isn't
- "or" filters together
- More exports, views
- Decent form validation

# Documentation

http://django-report-builder.readthedocs.org/en/2.x/

# Discussion

Let us know your thoughts at https://google.com/+Burkesoftware or consider sending some pull requests our way!
