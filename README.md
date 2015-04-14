django-report-builder
=====================

A GUI for Django ORM. Build custom queries and display results. 
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![Build Status](https://travis-ci.org/burke-software/django-report-builder.png?branch=master)](https://travis-ci.org/burke-software/django-report-builder) [![Bountysource](https://www.bountysource.com/badge/tracker?tracker_id=314767)](https://www.bountysource.com/trackers/314767-burke-software-django-report-builder?utm_source=314767&utm_medium=shield&utm_campaign=TRACKER_BADGE)

[Support development on gratipay](http://www.gratipay.com/bufke)

# News

3.0 has been released which features a rewritten user interface! 
For the old see the [2.x] branch.

## 3.0 Changes

- Frontend redone in angular and material design
- Async report status
- Requires Django 1.7 and Django Rest Framework 3.0. Users of older versions should continue to use the [2.x] branch instead. I will continue to accept pull requests for 2.x however new features will be added only in 3.x
- Responsive
- API built with DRF - in theory you could implement your own frontend
- Property fields must now be explicity allowed in settings
 
## Why a frontend redesign?

The older frontend featured jquery functions that inserted raw copy and pasted html code and even had a name vs field_name reversal bug. This rewrite will help with maintainability and adding new features. Also it's a lot faster since you never need to reload the page. If you'd prefer a non angular front-end your pull request is welcome.

That said the django 1.7 and rest framework 3.0 requirements are tough and I plan to maintain 2.x for awhile.

## Upgrading

If you customized the html template this will certainly break it. Instructions for customization coming soon. I'd suggest just running the app as is or with a simple menu bar over top.

1. Ensure you are on the latest 2.x branch first and run south migrations.
2. Run django 1.7 migrations `./manage.py migrate`
 
There's actually no schema changes at all - but you'll want to be in sync with the 1.7 migrations as that is the future.

## What's next

- Or filtering
- More Testing

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

# Hacking

We've included a fig.yml file for use with [fig](http://fig.sh/). There's also a demo project so you can start using report builder right now without touching any python code.
Once you have fig installed just run `fig up`. Populate the database with `fig run --rm web ./manage.py migrate`. 
You may want to edit fig.yml to comment/uncomment the django-report-utils line. Report utils is a seperated library with common reporting functions. If you want to hack on report utils too just clone the repo in a sibling directory.

# Discussion

Let us know your thoughts at https://google.com/+Burkesoftware

[2.x]: https://github.com/burke-software/django-report-builder/tree/2.x
