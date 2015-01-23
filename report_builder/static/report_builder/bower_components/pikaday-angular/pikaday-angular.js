'use strict';

angular.module('angularPikaday', [])
  .provider('pikaday', function() {
    var config = {};

    this.$get = function() {
      return config;
    };

    this.setConfig = function setConfig(pikadayConfig) {
      config = pikadayConfig;
    };

  })
  .directive('pikaday', ['pikaday', function(pikaday) {
  return {
    restrict: 'A',
    scope: {
      pikaday: '=',
    },
    link: function (scope, elem, attrs) {

      var picker = new Pikaday({

        field: elem[0],
        trigger: document.getElementById(attrs.triggerId),
        bound: attrs.bound !== 'false',
        position: attrs.position || '',
        format: attrs.format || 'ddd MMM D YYYY', // Requires Moment.js for custom formatting
        defaultDate: new Date(attrs.defaultDate),
        setDefaultDate: attrs.setDefaultDate === 'true',
        firstDay: attrs.firstDay ? parseInt(attrs.firstDay) : 0,
        minDate: new Date(attrs.minDate),
        maxDate: new Date(attrs.maxDate),
        yearRange: attrs.yearRange ? JSON.parse(attrs.yearRange) : 10, // Accepts int (10) or 2 elem array ([1992, 1998]) as strings
        isRTL: attrs.isRTL === 'true',
        i18n: pikaday.i18n || {
          previousMonth : 'Previous Month',
          nextMonth     : 'Next Month',
          months        : ['January','February','March','April','May','June','July','August','September','October','November','December'],
          weekdays      : ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
          weekdaysShort : ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        },
        yearSuffix: attrs.yearSuffix || '',
        showMonthAfterYear: attrs.showMonthAfterYear === 'true',

        onSelect: function () {
          setTimeout(function(){
            scope.$apply();
          });
        }
      });
      scope.pikaday = picker;

      scope.$on('$destroy', function () {
        picker.destroy();
      });
    }
  };
}]);
