django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might 
not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder)

# News

I'm starting another report related Django project to create a framework for more customized, less flexible, and 
easier to use reports. Interested? Check it out this:
https://github.com/burke-software/django-report-builder/issues/77

Of course Report Builder is still dear to my heart. The two projects are doing very seperate use cases.
Hopefully I'll have time to update soon. Pull requests are always welcome :)

# What is Django Report Builder?

![](https://raw.github.com/burke-software/django-report-builder/master/screenshots/reportbuilderscreen.png)

What's finished?
- Add filters
- Add display fields
- Preview and create xlsx reports
- Very simple security, user must have change or "view" permission to view 
reports. Unprivileged users can still build reports and see database schema.
- Model properties (thanks yekibud)
- Support for [django-custom-fields](http://code.google.com/p/django-custom-field/)
- Export to Report global admin action

What isn't
- "or" filters together
- More exports, views
- Decent form validation

# Documentation

http://django-report-builder.readthedocs.org/

# Discussion

Let us know your thoughts at https://google.com/+Burkesoftware or consider sending some pull requests our way!
