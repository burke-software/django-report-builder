# django-report-builder

A GUI for Django ORM. Build custom queries and display results.
Targets sys admins and capable end users who might not be able to program or gain direct interactive shell access.

[![pipeline status](https://gitlab.com/burke-software/django-report-builder/badges/master/pipeline.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)
[![coverage report](https://gitlab.com/burke-software/django-report-builder/badges/master/coverage.svg)](https://gitlab.com/burke-software/django-report-builder/commits/master)

Status: Unmaintained and does not support the latest Django version. I haven't used this project personally for many years. Please open an issue if you can help contribute or wish to take over the project entirely.

# News

## 6.5 (unreleased)

- Add Django 4.x support. Django 3.2 is still supported. Thanks @jeanwainer

## 6.4.2

- Fixes to CI pipeline

## 6.4

- Added Django 3.0 and 3.1 support. Django 1.11 and 2.2 are still supported. This will likely be the last release to support 1.11.

View more on the [CHANGELOG](CHANGELOG).

# What is Django Report Builder?

![](docs/screenshots/reportbuilderscreen.jpg)

## Features

* Add filters
* Add display fields
* Preview and create xlsx reports
* Uses Django permissions models - Staff users must have "change" or "view" permission to view
  reports. Unprivileged users can still build reports and see database schema.
   * Report builder is intended for generally trusted staff users and requires is_staff to be set.
* Export to Report global admin action
* Scheduled reports can generate and send to users on cron like schedule
* Optional asynchronous report generation

# Documentation

http://django-report-builder.readthedocs.org/

[Google group](https://groups.google.com/forum/#!forum/django-report-builder/).

[Contributing](http://django-report-builder.readthedocs.org/en/latest/contributors/)

## Development quick start

This package uses Django in Docker and Angular CLI for development purposes.

1. Start docker `docker-compose up`
2. Migrate and  create an admin user `docker-compose run --rm web ./manage.py migrate`
3. Start the Angular CLI server. Ensure Node is installed. `cd js`, `yarn`, `yarn start`
4. Django runs on port 8000 by default. Go to localhost:8000/admin and log in.
5. Angular runs on port 4200. Now that you are logged in, go to localhost:4200

More detailed instructions are at [here](https://django-report-builder.readthedocs.io/en/latest/contributors/)
