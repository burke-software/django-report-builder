#!/bin/bash
export C_FORCE_ROOT="true"
celery -A report_builder_demo worker -l info&
python manage.py runserver_plus 0.0.0.0:8000
