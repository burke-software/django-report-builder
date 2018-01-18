#Understanding the endpoints

This page explains how to interact with the endpoints that come with report builder. It may be useful if you are extending report builder or creating your own front end.

-------------

Initial path from root: `/report_builder/api/`

-------------

**Get all reports**:

`/report_builder/api/report` GET

Sample response:

```json
[
    {
        "id": 1,
        "name": "trial",
        "modified": "2015-06-08",
        "root_model": 19,
        "root_model_name": "account",
        "displayfield_set": [
            {
                "id": 33,
                "path": "orders__",
                "path_verbose": "order",
                "field": "dropbox_url",
                "field_verbose": "dropbox url",
                "name": "dropbox_url",
                "sort": null,
                "sort_reverse": false,
                "width": 15,
                "aggregate": "",
                "position": 0,
                "total": false,
                "group": false,
                "report": 1,
                "display_format": null,
                "field_type": "CharField"
            },
            ... etc ...
        ],
        "distinct": false,
        "user_created": 328,
        "user_modified": null,
        "filterfield_set": [
            {
                "id": 16,
                "path": "account__",
                "path_verbose": "account",
                "field": "id",
                "field_verbose": "ID",
                "field_type": "AutoField",
                "filter_type": "gt",
                "filter_value": "1",
                "filter_value2": "",
                "exclude": false,
                "position": 0,
                "report": 1
            }
        ],
        "report_file": null,
        "report_file_creation": null
    },
    ... etc ...
]
```

-------------

**New report**:

`/report_builder/api/report` POST with data

  - name
  - description (not required)
  - root_model

Sample request:

```json
{
  "name": "c",
  "description": "d",
  "root_model": "33"
}
```

Sample response:

```json
{
    "id": 18,
    "name": "c",
    "modified": "2015-06-08",
    "root_model": 33,
    "root_model_name": "Account",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 328,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": null,
    "report_file_creation": null
}
```

-------------

**Get report**:

`/report_builder/api/report/<id>` GET

sample response where <id> = 17:

```json
{
    "id": 17,
    "name": "gg",
    "modified": "2015-06-08",
    "root_model": 33,
    "root_model_name": "Account",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 328,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": null,
    "report_file_creation": null
}
```

-------------

**Get related fields (to a model):**

`/report_builder/api/related_fields/` POST with data

Sample request:

```json
{
    "model": 33,
    "path": "",
    "path_verbose": "",
    "field": ""
}
```

Sample response:

```json
[
    {
        "help_text": "",
        "verbose_name": "account_masterrecord_set",
        "model_id": 33,
        "field_name": "account_masterrecord_set",
        "path": ""
    },
    {
        "help_text": "",
        "verbose_name": "account_parent_set",
        "model_id": 33,
        "field_name": "account_parent_set",
        "path": ""
    },
    {
        "help_text": "",
        "verbose_name": "accountcontactrole_set",
        "model_id": 33,
        "field_name": "accountcontactrole",
        "path": ""
    },
    ... etc ...
]
```

-------------

**Get fields (of a model):**

`/report_builder/api/fields` POST with data

Sample request:

```json
{
    "model": 33,
    "path": "",
    "path_verbose": "",
    "field": ""
}
```

Sample response:

```json
[
    {
        "field_type": "CharField",
        "name": "account_manager",
        "path_verbose": "",
        "field": "account_manager",
        "help_text": "",
        "path": "",
        "field_verbose": "Account Manager"
    },
    {
        "field_type": "CharField",
        "name": "account_rank",
        "path_verbose": "",
        "field": "account_rank",
        "help_text": "",
        "path": "",
        "field_verbose": "Account Rank"
    },
    {
        "field_type": "CharField",
        "name": "account_source",
        "path_verbose": "",
        "field": "account_source",
        "help_text": "",
        "path": "",
        "field_verbose": "Account Source"
    },
    ... etc ...
]
```

-------------

**Save report:**

`/report_builder/api/report/<id>` PUT with data:

Sample request (when model is Account, and adding Billing City):

more fields that you add such as Billing City, website means that it goes into
displayfield_set.

```json
{
    "id": 18,
    "name": "c",
    "modified": "2015-06-08",
    "root_model": 33,
    "root_model_name": "Account",
    "displayfield_set": [
        {
            "field_type": "CharField",
            "name": "billing_city",
            "path_verbose": "",
            "field": "billing_city",
            "help_text": "",
            "path": "",
            "field_verbose": "Billing City",
            "report": 18,
            "position": 0
        }
    ],
    "distinct": false,
    "user_created": 328,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": null,
    "report_file_creation": null,
    "lastSaved": null
}
```

Suppose I add website with Billing City then the displayfield_set becomes:

```json
"displayfield_set": [
    {
        "field_type": "DateTimeField",
        "name": "system_modstamp",
        "path_verbose": "",
        "field": "system_modstamp",
        "help_text": "",
        "path": "",
        "field_verbose": "System Modstamp",
        "report": 22,
        "position": 0
    },
    {
        "field_type": "CharField",
        "name": "website",
        "path_verbose": "",
        "field": "website",
        "help_text": "",
        "path": "",
        "field_verbose": "Website",
        "report": 22,
        "position": 1
    }
]
```

Sample response:

```json
{
    "id": 18,
    "name": "c",
    "modified": "2015-06-08",
    "root_model": 33,
    "root_model_name": "Account",
    "displayfield_set": [
        {
            "id": 37,
            "path": "",
            "path_verbose": "",
            "field": "billing_city",
            "field_verbose": "Billing City",
            "name": "billing_city",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 18,
            "display_format": null,
            "field_type": "CharField"
        }
    ],
    "distinct": false,
    "user_created": 328,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": null,
    "report_file_creation": null
}
```

-------------

**Generate report data:**

`report_builder/api/report/<id>/generate/` GET

Sample response:

```json
{
    "meta": {
        "titles": [
            "billing_city"
        ]
    },
    "data": [
        [
            "Toronto"
        ],
        [
            "Mountain view"
        ],
        ... etc ...
    ]
}
```

-------------

**Add DisplayFields to a report**

`report_builder/api/report/<id>` PUT

Sample request:

If your previous response from when you did a GET on `report_builder/api/report/<id>` was:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

If you want to add a `displayfield_set` then the request for the PUT to add the `displayfield_set` is:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "field_type": "AutoField",
            "name": "id",
            "path_verbose": "",
            "field": "id",
            "help_text": "",
            "path": "",
            "field_verbose": "ID",
            "report": 2,
            "position": 1
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z",
    "lastSaved": "2015-06-24T19:55:43.693Z"
}
```

It will give you a response like:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 75,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

And to add another field to the `displayfield_set`:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 75,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        },
        {
            "field_type": "Property",
            "name": "i_want_char_field",
            "path_verbose": "",
            "field": "i_want_char_field",
            "help_text": "Adding this property will significantly increase the time it takes to run a report.",
            "path": "",
            "field_verbose": "i_want_char_field",
            "report": 2,
            "position": 1,
            "can_filter": true,
            "field_choices": true,
            "is_default": true
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z",
    "lastSaved": "2015-06-24T20:31:54.887Z"
}
```

The response to that PUT would be:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 76,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        },
        {
            "id": 77,
            "path": "",
            "path_verbose": "",
            "field": "i_want_char_field",
            "field_verbose": "i_want_char_field",
            "name": "i_want_char_field",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 1,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "Property"
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

Where do you get the details to add? When you do a POST to get the `/fields` and it gives you back the information you get this:

```json
[
    {
        "field_type": "AutoField",
        "name": "id",
        "path_verbose": "",
        "field": "id",
        "help_text": "",
        "path": "",
        "field_verbose": "ID"
        "can_filter": true,
        "field_choices": true,
        "is_default": true
    },
    {
        "field_type": "Property",
        "name": "i_want_char_field",
        "path_verbose": "",
        "field": "i_want_char_field",
        "help_text": "Adding this property will significantly increase the time it takes to run a report.",
        "path": "",
        "field_verbose": "i_want_char_field"
        "can_filter": true,
        "field_choices": true,
        "is_default": true
    },
  ... etc ...
]
```

You literally take one of those elements and append it to the `displayfield_set` array, and PUT it back. Now we have to deal with custom field elements. 

```json
"displayfield_set": [
    {
        "id": 37,
        "path": "",
        "path_verbose": "",
        "field": "id",
        "field_verbose": "ID",
        "name": "id",
        "sort": null,
        "sort_reverse": false,
        "width": 15,
        "aggregate": "",
        "position": 0,
        "total": false,
        "group": false,
        "report": 2,
        "display_format": null,
        "field_type": "AutoField"
    }
]
```

The field `displayfield_set` is a little different from `filterfield_set`, which we will look at next.

Ignore the fields `total`, and `group`, and always set them as `false`. Whenever you do a PUT it will give you back a response, and you should always just replace your current report json (that you have saved) with the response.

Fields specific to `displayfield_set` are:

```python
fields = ('id', 'path', 'path_verbose', 'field', 'field_verbose',
      'name', 'sort', 'sort_reverse', 'width', 'aggregate',
         'position', 'total', 'group', 'report', 'display_format',
         'field_type')
read_only_fields = ('id')
```

For the `displayfield_set` you initially only need:

```json
{
    "field_type": "Property",
    "name": "i_want_char_field",
    "path_verbose": "",
    "field": "i_want_char_field",
    "help_text": "Adding this property will significantly increase the time it takes to run a report.",
    "path": "",
    "field_verbose": "i_want_char_field",
    "report": 2,
    "position": 1
}
```

Fields gives you:

```json
{
  "field_type": "Property",
  "name": "i_want_char_field",
  "path_verbose": "",
  "field": "i_want_char_field",
  "help_text": "Adding this property will significantly increase the time it takes to run a report.",
  "path": "",
  "field_verbose": "i_want_char_field",
  "can_filter": true,
  "field_choices": true,
  "is_default": true
}
```

So the only difference in fields is: `report` and `position`. The position can just be calculated by looking at the length of the `displayfield_set` before adding this element and then adding one. The `report` is the ID of the report. 

This is only in the initial PUT when they add things. If they have customized settings before they save then you have to add new detials. 

They can edit:

```json
'name', 'sort', 'sort_reverse', 'width', 'aggregate', 'position'
```

`sort` is an integer. If you have 3 columns `a`, `b`, `c` the `sort` integer for each is the importance of which is sorted first. So if the sort for `c` is `1` then it will get sorted first, and then `b`, and then `c`. 

People can rename columns using `name` rather than the default names.

`sort_reverse` is obvious. Could be useful for things like `DateTimeField`.

Leave `aggregate` for now.

`position` is important if you want to rearrange them.

You can PUT fields `can_filter`, `field_choices`, `is_default` alongside everything else. They just will dissapear in the response so keep them safe somewhere else.

### Adding external fields from other models to the report

**THIS ONLY WORKS FOR ONE LEVEL DEEP** If you're trying to go beyond the one level I will update the documentation soon. Right now if you're at Order it could only go to models directly having an association with Order.

The same procedure here as the one above, but the way to get the `/fields/` is very different. This is only because it adds on a `path` variable on the object.

So from the information that you have in your current report you know that the `root_model` is 9 (for example).

To get all the fields that are in that current model make a request to `/related_fields` with POST:

```json
{
    "model": 9,
    "path": "",
    "path_verbose": "",
    "field": ""
}
```

It would give a response like this:

```json
[
    {
        "model_id": 9,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "",
        "help_text": "",
        "verbose_name": "foos",
        "field_name": "foos",
        "parent_model_name": "foos"
    }
]
```

These are the fields that are in the model (with the id 9) that have some kind of relationship with an external model. 

If you want to get the fields for the `field_name` foos, which is related to the `parent_model_name` foos then you would do:

A POST on `/related_fields` with the data:

```json
{
    "model": 9,
    "path": "",
    "field": "foos"
}
```

Where the `model` is the ID of the root_model, and the `field` is the `field_name` that you get above. (Stupid inconsistency even in naming)

This would give you back all the fields (not related_fields as well) for the model `foos`.

```json
[
    {
        "can_filter": true,
        "field": "char_field2",
        "help_text": "",
        "field_choices": [],
        "name": "char_field2",
        "path_verbose": "foo",
        "field_type": "CharField",
        "is_default": true,
        "path": "foos__",
        "field_verbose": "char field2"
    },
    {
        "can_filter": true,
        "field": "char_field",
        "help_text": "",
        "field_choices": [],
        "name": "char_field",
        "path_verbose": "foo",
        "field_type": "CharField",
        "is_default": true,
        "path": "foos__",
        "field_verbose": "char field"
    },
  ... etc ...
]
```

Notice that they have now added a `path`. This is important when you're adding things to `displayfield_set`. You can just append these to `displayfield_set` array and they would work. 

To get the `/related_fields` you do the same thing.

You do a POST on the related_fields end-point using the data:

```json
{
    "model": 9,
    "path": "",
    "field": "foos"
}
```

The data to get the data is exactly the same as `/fields`.

The data it gives you back is:

```json
[
    {
        "model_id": 7,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "foos__",
        "help_text": "",
        "verbose_name": "bar_set",
        "field_name": "bar",
        "parent_model_name": "bar"
    },
    {
        "model_id": 7,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "foos__",
        "help_text": "",
        "verbose_name": "fooexclude",
        "field_name": "fooexclude",
        "parent_model_name": "fooexclude"
    }
]
```

Notice that now they have added a `path`. 

**Add DisplayFields to a report**

`report_builder/api/report/<id>` PUT

Sample request:

If your previous response from when you did a GET on `report_builder/api/report/<id>` was:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

If you want to add a `displayfield_set` then the request for the PUT to add the `displayfield_set` is:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "field_type": "AutoField",
            "name": "id",
            "path_verbose": "",
            "field": "id",
            "help_text": "",
            "path": "",
            "field_verbose": "ID",
            "report": 2,
            "position": 1
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z",
    "lastSaved": "2015-06-24T19:55:43.693Z"
}
```

It will give you a response like:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 75,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

And to add another field to the `displayfield_set`:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 75,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        },
        {
            "field_type": "Property",
            "name": "i_want_char_field",
            "path_verbose": "",
            "field": "i_want_char_field",
            "help_text": "Adding this property will significantly increase the time it takes to run a report.",
            "path": "",
            "field_verbose": "i_want_char_field",
            "report": 2,
            "position": 1,
            "can_filter": true,
            "field_choices": true,
            "is_default": true
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z",
    "lastSaved": "2015-06-24T20:31:54.887Z"
}
```

The response to that PUT would be:

```json
{
    "id": 2,
    "name": "sssf",
    "description": "",
    "modified": "2015-06-24",
    "root_model": 9,
    "root_model_name": "bar",
    "displayfield_set": [
        {
            "id": 76,
            "path": "",
            "path_verbose": "",
            "field": "id",
            "field_verbose": "ID",
            "name": "id",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 0,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "AutoField"
        },
        {
            "id": 77,
            "path": "",
            "path_verbose": "",
            "field": "i_want_char_field",
            "field_verbose": "i_want_char_field",
            "name": "i_want_char_field",
            "sort": null,
            "sort_reverse": false,
            "width": 15,
            "aggregate": "",
            "position": 1,
            "total": false,
            "group": false,
            "report": 2,
            "display_format": null,
            "field_type": "Property"
        }
    ],
    "distinct": false,
    "user_created": 1,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": "http://localhost:8080/media/report_files/sssf_9c8XUkg.xlsx",
    "report_file_creation": "2015-06-23T17:14:23.727217Z"
}
```

Where do you get the details to add? When you do a POST to get the `/fields` and it gives you back the information you get this:

```json
[
    {
        "field_type": "AutoField",
        "name": "id",
        "path_verbose": "",
        "field": "id",
        "help_text": "",
        "path": "",
        "field_verbose": "ID"
        "can_filter": true,
        "field_choices": true,
        "is_default": true
    },
    {
        "field_type": "Property",
        "name": "i_want_char_field",
        "path_verbose": "",
        "field": "i_want_char_field",
        "help_text": "Adding this property will significantly increase the time it takes to run a report.",
        "path": "",
        "field_verbose": "i_want_char_field"
        "can_filter": true,
        "field_choices": true,
        "is_default": true
    },
  ... etc ...
]
```

You literally take one of those elements and append it to the `displayfield_set` array, and PUT it back. Now we have to deal with custom field elements. 

```json
"displayfield_set": [
    {
        "id": 37,
        "path": "",
        "path_verbose": "",
        "field": "id",
        "field_verbose": "ID",
        "name": "id",
        "sort": null,
        "sort_reverse": false,
        "width": 15,
        "aggregate": "",
        "position": 0,
        "total": false,
        "group": false,
        "report": 2,
        "display_format": null,
        "field_type": "AutoField"
    }
]
```

The field `displayfield_set` is a little different from `filterfield_set`, which we will look at next.

Ignore the fields `total`, and `group`, and always set them as `false`. Whenever you do a PUT it will give you back a response, and you should always just replace your current report json (that you have saved) with the response.

Fields specific to `displayfield_set` are:

```python
fields = ('id', 'path', 'path_verbose', 'field', 'field_verbose',
      'name', 'sort', 'sort_reverse', 'width', 'aggregate',
         'position', 'total', 'group', 'report', 'display_format',
         'field_type')
read_only_fields = ('id')
```

For the `displayfield_set` you initially only need:

```json
{
    "field_type": "Property",
    "name": "i_want_char_field",
    "path_verbose": "",
    "field": "i_want_char_field",
    "help_text": "Adding this property will significantly increase the time it takes to run a report.",
    "path": "",
    "field_verbose": "i_want_char_field",
    "report": 2,
    "position": 1
}
```

Fields gives you:

```json
{
  "field_type": "Property",
  "name": "i_want_char_field",
  "path_verbose": "",
  "field": "i_want_char_field",
  "help_text": "Adding this property will significantly increase the time it takes to run a report.",
  "path": "",
  "field_verbose": "i_want_char_field",
  "can_filter": true,
  "field_choices": true,
  "is_default": true
}
```

So the only difference in fields is: `report` and `position`. The position can just be calculated by looking at the length of the `displayfield_set` before adding this element and then adding one. The `report` is the ID of the report. 

This is only in the initial PUT when they add things. If they have customized settings before they save then you have to add new details. 

They can edit:

```json
'name', 'sort', 'sort_reverse', 'width', 'aggregate', 'position'
```

`sort` is an integer. If you have 3 columns `a`, `b`, `c` the `sort` integer for each is the importance of which is sorted first. So if the sort for `c` is `1` then it will get sorted first, and then `b`, and then `c`. 

People can rename columns using `name` rather than the default names.

`sort_reverse` is obvious. Could be useful for things like `DateTimeField`.

Leave `aggregate` for now.

`position` is important if you want to rearrange them.

You can PUT fields `can_filter`, `field_choices`, `is_default` alongside everything else. They just will dissapear in the response so keep them safe somewhere else.

### Adding external fields from other models to the report

**THIS ONLY WORKS FOR ONE LEVEL DEEP** If you're trying to go beyond the one level I will update the documentation soon. Right now if you're at Order it could only go to models directly having an association with Order.

The same procedure here as the one above, but the way to get the `/fields/` is very different. This is only because it adds on a `path` variable on the object.

So from the information that you have in your current report you know that the `root_model` is 9 (for example).

To get all the fields that are in that current model make a request to `/related_fields` with POST:

```json
{
    "model": 9,
    "path": "",
    "path_verbose": "",
    "field": ""
}
```

It would give a response like this:

```json
[
    {
        "model_id": 9,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "",
        "help_text": "",
        "verbose_name": "foos",
        "field_name": "foos",
        "parent_model_name": "foos"
    }
]
```

These are the fields that are in the model (with the id 9) that have some kind of relationship with an external model. 

If you want to get the fields for the `field_name` foos, which is related to the `parent_model_name` foos then you would do:

A POST on `/related_fields` with the data:

```json
{
    "model": 9,
    "path": "",
    "field": "foos"
}
```

Where the `model` is the ID of the root_model, and the `field` is the `field_name` that you get above. (Stupid inconsistency even in naming)

This would give you back all the fields (not related_fields as well) for the model `foos`.

```json
[
    {
        "can_filter": true,
        "field": "char_field2",
        "help_text": "",
        "field_choices": [],
        "name": "char_field2",
        "path_verbose": "foo",
        "field_type": "CharField",
        "is_default": true,
        "path": "foos__",
        "field_verbose": "char field2"
    },
    {
        "can_filter": true,
        "field": "char_field",
        "help_text": "",
        "field_choices": [],
        "name": "char_field",
        "path_verbose": "foo",
        "field_type": "CharField",
        "is_default": true,
        "path": "foos__",
        "field_verbose": "char field"
    },
  ... etc ...
]
```

Notice that they have now added a `path`. This is important when you're adding things to `displayfield_set`. You can just append these to `displayfield_set` array and they would work.

To get the `/related_fields` you do the same thing.

You do a POST on the related_fields end-point using the data:

```json
{
    "model": 9,
    "path": "",
    "field": "foos"
}
```

The data to get the data is exactly the same as `/fields`.

The data it gives you back is:

```json
[
    {
        "model_id": 7,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "foos__",
        "help_text": "",
        "verbose_name": "bar_set",
        "field_name": "bar",
        "parent_model_name": "bar"
    },
    {
        "model_id": 7,
        "parent_model_app_label": false,
        "included_model": true,
        "path": "foos__",
        "help_text": "",
        "verbose_name": "fooexclude",
        "field_name": "fooexclude",
        "parent_model_name": "fooexclude"
    }
]
```

Notice that now they have added a `path`. HOWEVER: here it gives you back a new `model_id` that you need to use for all the levels below. 

**Second level**

Take the new `model_id`, and `path` that we get from one of the fields in `related_fields`, and now we have to use that. Basically the new `model_id` represents the `model_id` of the model Foo. We started off with the model Bar and the field `foos` that was a ManyToMany relationship with Foo. Now that we have gotten the `related_fields` of the model Foo, we also get the `model_id` of it.

Now we're in the territory of getting details of the model `FooExclude`. We have to append the `path` variable because we have to keep into consideration that we're adding this to the report, and the report has a base of `Bar`. So now we're looking into the `/fields` of `FooExclude`, which is one of the models in `/related_field` of `Foo`.

```json
{
    "model": 7,
    "path": "foos__",
    "field": "fooexclude"
}
```

So you append the `path` that we had earlier. In this way as deep as we go down we'll just keep appending the `path` variable.

The response you get from that is:

```json
[
    {
        "can_filter": true,
        "field": "char_field",
        "help_text": "",
        "field_choices": [],
        "name": "char_field",
        "path_verbose": "fooexclude",
        "field_type": "CharField",
        "is_default": true,
        "path": "foos__fooexclude__",
        "field_verbose": "char field"
    }
]
```

So now we can see that the `path` variable has had even more additions. 

**Add FilterFields to a report**

`report_builder/api/report/<id>` PUT

Sample request:

If your previous response from when you did a GET on `report_builder/api/report/<id>` was:

The normal report:

```json
{
    "id": 14,
    "name": "apples",
    "description": "",
    "modified": "2015-06-30",
    "root_model": 19,
    "root_model_name": "account",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 338,
    "user_modified": null,
    "filterfield_set": [],
    "report_file": null,
    "report_file_creation": null
}
```

Adding to the `filterfield_set` array is the same as adding to the `displayfield_set` array. When you add a `filterfield_set` you need the following:

There are certain fields that cannot be blank.

You have to set a filter type, and a value for that filter type for each filter field.

So if I add a field the request would be:

```json
{
    "id": 14,
    "name": "apples",
    "description": "",
    "modified": "2015-06-30",
    "root_model": 19,
    "root_model_name": "account",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 338,
    "user_modified": null,
    "filterfield_set": [
        {
            "is_default": false,
            "field": "industry",
            "can_filter": true,
            "field_choices": [],
            "name": "industry",
            "path_verbose": "",
            "field_type": "CharField",
            "help_text": "",
            "path": "",
            "field_verbose": "industry",
            "report": 14,
            "filter_type": "exact",
            "filter_value": "CPG",
            "position": 0
        }
    ],
    "report_file": null,
    "report_file_creation": null,
    "lastSaved": null
}
```

Where you would take the values you get from the `/fields` request you made to get that field, and add a couple more fields into it:

```json
{
  "is_default": false,
  "field": "industry",
  "can_filter": true,
  "field_choices": [],
  "name": "industry",
  "path_verbose": "",
  "field_type": "CharField",
  "help_text": "",
  "path": "",
  "field_verbose": "industry",
  "report": 14,
  "filter_type": "exact",
  "filter_value": "CPG",
  "position": 0
}
```

`filter_value`, and `filter_type` have to be there or the request will fail. 

The response will be:

```json
{
    "id": 14,
    "name": "apples",
    "description": "",
    "modified": "2015-06-30",
    "root_model": 19,
    "root_model_name": "account",
    "displayfield_set": [],
    "distinct": false,
    "user_created": 338,
    "user_modified": null,
    "filterfield_set": [
        {
            "id": 21,
            "path": "",
            "path_verbose": "",
            "field": "industry",
            "field_verbose": "industry",
            "field_type": "CharField",
            "filter_type": "exact",
            "filter_value": "CPG",
            "filter_value2": "",
            "exclude": false,
            "position": 0,
            "report": 14
        }
    ],
    "report_file": null,
    "report_file_creation": null
}
```

The `filter_type`s that are possible are returned when you do an OPTIONS on `/filterfields/`. The exact are there is the field `filter_type`. You have to use one of those values as the `filter_type`. 

**Exporting using xlsx**

Reports will download either directly or asynchronously. This is defined by `REPORT_BUILDER_ASYNC_REPORT` in settings.py

Request a report by making a GET request to `/report_builder/report/<id>/download_file/xlsx/` (or /csv/)

When async is false - the response will be the actual xlsx or csv file.

When async is true - the GET request triggers a celery task to process the report. The response will be:

```json
{
    "task_id": "feef7db6-fe8c-4a81-8dea-ca67d393674d"
}
```

`task_id` is the celery task id which can be used to check when the task is finished (or errored).

Check the status of a report with `/report_builder/report/<report_id>/check_status/<task_id>/`
