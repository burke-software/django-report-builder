# ngHandsontable - the AngularJS directive for [Handsontable](https://github.com/handsontable/handsontable)

Enables creation of data grid applications in AngularJS.

## Demo

See the demo at http://handsontable.github.io/ngHandsontable

## Usage

Include the library files:

```html
<link rel="stylesheet" media="screen" href="bower_components/handsontable/dist/handsontable.full.css">
<script src="bower_components/angular/angular.js"></script>
<script src="bower_components/handsontable/dist/handsontable.full.js"></script>
<script src="dist/ngHandsontable.js"></script>
```

Template:

```html
<hot-table
    settings="{colHeaders: colHeaders, contextMenu: ['row_above', 'row_below', 'remove_row'], afterChange: afterChange }"
    rowHeaders="false"
    minSpareRows="minSpareRows"
    datarows="db.items"
    height="300"
    width="700">
    <hot-column data="id"                  title="'ID'"></hot-column>
    <hot-column data="name.first"          title="'First Name'"  type="grayedOut"  readOnly></hot-column>
    <hot-column data="name.last"           title="'Last Name'"   type="grayedOut"  readOnly></hot-column>
    <hot-column data="address"             title="'Address'" width="150"></hot-column>
    <hot-column data="product.description" title="'Favorite food'" type="'autocomplete'">
        <hot-autocomplete datarows="description in product.options"></hot-autocomplete>
    </hot-column>
    <hot-column data="price"               title="'Price'"     type="'numeric'"  width="80"  format="'$ 0,0.00'" ></hot-column>
    <hot-column data="isActive"            title="'Is active'" type="'checkbox'" width="65"  checkedTemplate="'Yes'" uncheckedTemplate="'No'"></hot-column>
</hot-table>
```

Controller:

```javascript
$scope.db.items = [
  {
    "id":1,
    "name":{
      "first":"John",
      "last":"Schmidt"
    },
    "address":"45024 France",
    "price":760.41,
    "isActive":"Yes",
    "product":{
      "description":"Fried Potatoes",
      "options":[
        {
          "description":"Fried Potatoes",
          "image":"//a248.e.akamai.net/assets.github.com/images/icons/emoji/fries.png",
          "Pick$":null
        },
        {
          "description":"Fried Onions",
          "image":"//a248.e.akamai.net/assets.github.com/images/icons/emoji/fries.png",
          "Pick$":null
        }
      ]
    }
  },
  //more items go here
];
```
  
## Directives and attributes specification

All **Handsontable** options listed [here](https://github.com/handsontable/jquery-handsontable/wiki) should be supported
  
 Directive                       | Attribute&nbsp;&nbsp;&nbsp; | Description
 --------------------------------|-----------------------------|-------------
 **&lt;div hot-table&gt;**       |                             | Defines the grid container. Can also be declared as element `<ui-handsontable>`
 &lt;div hot-table&gt;           | datarows                    | Data provider for the grid. Usage like `item in items` (similar to ngRepeat). Creates new scope for each row
 &lt;div hot-table&gt;           | settings                    | jquery-handsontable settings. For list of options, see: [handsontable/jquery-handsontable](https://github.com/handsontable/jquery-handsontable)
 &lt;div hot-table&gt;           | selectedIndex               | Allows to bind a scope variable to get/set selected row index
 **&lt;hot-column&gt;**          |                             | Defines a column in the grid
 &lt;hot-column&gt;              | type                        | Column type. Possible values: `text`, `checkbox`, `autocomplete` (default: `text`)
 &lt;hot-column&gt;              | value                       | Row property that will be used as data source for each cell
 &lt;hot-column&gt;              | title                       | Column title
 &lt;hot-column&gt;              | readOnly                    | If set, column will be read-only
 &lt;hot-column&gt;              | saveOnBlur                  | (Autocomplete columns only) If set, `value` will be updated after autocomplete is blured. This is in contrast to default behavior, where `value` is updated after each keystroke
 &lt;hot-column&gt;              | strict                      | (Autocomplete columns only) If set, `value` can only be selected from autocomplete options. If not set, also custom `value` is allowed if entered to the text box
 &lt;hot-column&gt;              | checkedTemplate             | (Checkbox columns only) Expression that will be used as the value for checked `checkbox` cell (default: boolean `true`)
 &lt;hot-column&gt;              | uncheckedTemplate           | (Checkbox columns only) Expression that will be used as the value for unchecked `checkbox` cell (default: boolean `false`)

## License

The MIT License (see the [LICENSE](https://github.com/handsontable/ngHandsontable/blob/master/LICENSE) file for the full text)