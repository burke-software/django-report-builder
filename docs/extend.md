#Extending and integrating django-report-builder

Format 
------

Note many python format features require >= 2.7
http://docs.python.org/2/library/string.html#string-formatting

You may add formats in /admin/report_builder/format. See http://docs.python.org/2/library/string.html#format-examples

There are also some examples included in the south migrations. If you use south django-report-builder comes with
a few formats for you.

Integrations
------------

In most cases extending `/report_builder/base.html` should be enough. 
In this example I could expend the my_awesome_site template and ensure a header shows above the report builder.
Notice I must set the report builder content height with calc. 
If you know a way to fill all remaining viewport height without this do let me know!

Blocks angular_app, body, and nav are in my_awesome_site. 
Blocks report_header and content are part of report builder.

```
{% extends "my_awesome_site.html" %}
{% load static from staticfiles %}

{% block angular_app %}
    {% block report_header %}
    {% endblock %}
{% endblock %}

{% block body %}
    <div style="height: 62px">
    {% block nav %}
        {{ block.super }}
    {% endblock %}
    </div>
    <div style="height: calc(100% - 106px); margin-top: -20px;">
    {% block content %}
    {% endblock %}
    </div>
{% endblock %}
```

Report builder will run it's own angular app. If my_awesome_site also contained angular app it would not work. 
If for someone reason you want to run your angular apps with report builder's you will have to extend a lot more.
