## __pikaday-angular__ [working examples](http://nverba.github.io/pikaday-angular/)
Tested and working with [Pikaday Release version 1.2.0](https://github.com/dbushell/Pikaday/releases/tag/1.2.0)

__pikaday-angular__ is an AngularJS directive wraper that aims to make using __Pikaday__ with __Angular__ as simple as possible, exposing __Pikaday's__ configurable features as HTML attributes, handled by the directive.

### __Pikaday__ [source code & documentation](https://github.com/dbushell/Pikaday)


## Basic usage

Include the `angularPikaday` module as a dependency.

```
app = angular.module('YourApp', ['angularPikaday'])
```

Include the `pikaday` attribute and assign a scope.

``` language-HTML
<input pikaday="myPickerObject">
```

The date string returned to the input field will be pre-formatted by __Pikaday__, although formatting can be configured manually with the `format` attribute, if __moment.js__ is included.

## i18n

If you want to customize the used wordings, you can inject a custom object via the `pikadayProvider`.

Example:

```
angular.module('YourApp', ['angularPikaday'])
  .config(['pikadayProvider', function(pikadayProvider) {
    pikadayProvider.setConfig({
      i18n: {
        previousMonth : 'Previous Month',
        nextMonth     : 'Next Month',
        months        : ['January','February','March','April','May','June','July','August','September','October','November','December'],
        weekdays      : ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
        weekdaysShort : ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
      }
  })
}])
```


## Methods

__pikaday-angular__ binds the Pikaday picker object to the named scope and supports several methods for retrieving and updating the date.

For example, the `myPickerObject.getDate()` method can be user to retrieve a JavaScript Date object, which can easily be formatted using Angular.js' built in formatters.


```
<span> Date = {{ myPickerObject.getDate() | date:'MM/dd/yyyy' }}</span>
```

To see a complete list of methods available to the __Pikaday__ object, check out the [Pikaday README on Github](https://github.com/dbushell/Pikaday).

## Available attributes

__pikaday-angular__ accepts most of __Pikaday's__ configuration options as HTML attributes.

- `trigger` use a different element to trigger opening the datepicker, see trigger example (defaults to directive DOM element)
- `bound` automatically show/hide the datepicker on field focus (default true)
- `position` preferred position of the datepicker relative to the form field, e.g.: top right, bottom right Note: automatic adjustment may occur to avoid datepicker from being displayed outside the viewport.
- `format` the default output format for .toString() and field value (requires Moment.js for custom formatting)
- `default-date` the initial date to view when first opened
- `set-default-date` make the defaultDate the initial selected value
- `first-day` first day of the week (0: Sunday, 1: Monday, etc)
- `min-date` the minimum/earliest date that can be selected
- `max-date` the maximum/latest date that can be selected
- `year-range` number of years either side of the year select drop down (e.g. 10) or array of upper/lower range (e.g. [1900,2012])
- `is-r-t-l` reverse the calendar for right-to-left languages (default false)
- `year-suffix` additional text to append to the year in the title
- `show-month-after-year` render the month after year in the title (default false)


Check out the [demo](http://nverba.github.io/pikaday-angular/) for some other examples.
