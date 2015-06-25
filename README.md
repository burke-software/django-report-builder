django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder) [![Bountysource](https://www.bountysource.com/badge/tracker?tracker_id=314767)](https://www.bountysource.com/trackers/314767-burke-software-django-report-builder?utm_source=314767&utm_medium=shield&utm_campaign=TRACKER_BADGE)
[![Coverage Status](https://coveralls.io/repos/burke-software/django-report-builder/badge.svg)](https://coveralls.io/r/burke-software/django-report-builder)


# News

We now have a [google group](https://groups.google.com/forum/#!forum/django-report-builder/). Please post suggestions, ask questions, and let me know how you're using django report builder. I'll make future announnments there.

# What is Django Report Builder?

![](docs/screenshots/reportbuilderscreen.png)

## Features

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

# Documentation

http://django-report-builder.readthedocs.org/

# [Hacking](http://django-report-builder.readthedocs.org/en/latest/hacking/)

## Making pull requests

This project is a bit complex and has many features that some people will depend on and others will never use.
As such please submit a unit test with your pull request if merited. New features need unit tests. Bug fixes should too to prevent an idiot like me from breaking it later. Travis should also pass, if it fails please explain why. Thanks :)

# Discussion

Let us know your thoughts at https://google.com/+Burkesoftware

[2.x]: https://github.com/burke-software/django-report-builder/tree/2.x
