.. _extend:

Extending and integrating django-report-builder
===============================================

Format 
------

Note many python format features require >= 2.7
http://docs.python.org/2/library/string.html#string-formatting

You may add formats in /admin/report_builder/format. See http://docs.python.org/2/library/string.html#format-examples

There are also some examples included in the south migrations. If you use south django-report-builder comes with
a few formats for you.

Integrations
------------

Give django-report-builder a native look and feel. django-sis shows a good example of a django-grappelli
like style.

https://github.com/burke-software/django-sis/tree/master/templates/report_builder

Note I use django-apptemplates in this example to specify which app template I'm extending.
