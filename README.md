django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. Targets sys admins and capable end users who might 
not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder)

# News

Just pushed 2.0 changes to master. Code has been refactored, why don't you test it out now before 
I push to pypi. Changes:

- Changing the base templates slightly (could cause you trouble if customized)
- Factoring out functions to django-report-utils
- Added experimental support for asynchronous report generation

The common functions will used in:

- django-scaffold-report - a tool to streamline complex customized reports
- django-admin-export - a super old tool I made that sucks and will be remade!

If I don't hear any complaints I will push 2.0 to pypi soon. If you have an outstanding pull request you may need to
resubmit it against the new code base.

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
