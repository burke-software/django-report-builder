angular.module('MassAutoComplete', [])
.directive('massAutocomplete', ["$timeout", "$window", "$document", "$q", function ($timeout, $window, $document, $q) {
  'use strict';

  return {
    restrict: "A",
    scope: { options: '&massAutocomplete' },
    transclude: true,
    template:
      '<span ng-transclude></span>' +
      '<div class="ac-container" ng-show="show_autocomplete && results.length > 0" style="position:absolute;">' +
        '<ul class="ac-menu">' +
          '<li ng-repeat="result in results" ng-if="$index > 0" ' +
            'class="ac-menu-item" ng-class="$index == selected_index ? \'ac-state-focus\': \'\'">' +
            '<a href ng-click="apply_selection($index)" ng-bind-html="result.label"></a>' +
          '</li>' +
        '</ul>' +
      '</div>',
    link: function (scope, element) {
      scope.container = angular.element(element[0].getElementsByClassName('ac-container')[0]);
    },
    controller: ["$scope", function ($scope) {
      var that = this;

      var KEYS = {
        TAB: 9,
        ESC: 27,
        ENTER: 13,
        UP: 38,
        DOWN: 40
      };

      var EVENTS = {
        KEYDOWN: 'keydown',
        RESIZE: 'resize',
        BLUR: 'blur'
      };

      var _user_options = $scope.options() || {};
      var user_options = {
        debounce_position: _user_options.debounce_position || 150,
        debounce_attach: _user_options.debounce_attach || 300,
        debounce_suggest: _user_options.debounce_suggest || 200,
        debounce_blur: _user_options.debounce_blur || 150
      };

      var current_element,
          current_model,
          current_options,
          previous_value,
          value_watch,
          last_selected_value;

      $scope.show_autocomplete = false;

      // Debounce - taken from underscore
      function debounce(func, wait, immediate) {
          var timeout;
          return function() {
              var context = this, args = arguments;
              var later = function() {
                  timeout = null;
                  if (!immediate) func.apply(context, args);
              };
              var callNow = immediate && !timeout;
              clearTimeout(timeout);
              timeout = setTimeout(later, wait);
              if (callNow) func.apply(context, args);
          };
      }

      function _position_autocomplete() {
        var rect = current_element[0].getBoundingClientRect(),
            scrollTop = $document[0].body.scrollTop || $document[0].documentElement.scrollTop || $window.pageYOffset,
            scrollLeft = $document[0].body.scrollLeft || $document[0].documentElement.scrollLeft || $window.pageXOffset,
            container = $scope.container[0];

        container.style.width = rect.width + 'px';
      }
      var position_autocomplete = debounce(_position_autocomplete, user_options.debounce_position);

      // Attach autocomplete behaviour to an input element.
      function _attach(ngmodel, target_element, options) {
        // Element is already attached.
        if (current_element === target_element) return;
        // Safe: clear previously attached elements.
        if (current_element) that.detach();
        // The element is still the active element.
        if (target_element[0] !== $document[0].activeElement) return;

        options.on_attach && options.on_attach();

        current_element = target_element;
        current_model = ngmodel;
        current_options = options;
        previous_value = ngmodel.$viewValue;

        $scope.results = [];
        $scope.selected_index = -1;
        bind_element();

        value_watch = $scope.$watch(
          function () {
            return ngmodel.$modelValue;
          },
          function (nv, ov) {
            // Prevent suggestion cycle when the value is the last value selected.
            // When selecting from the menu the ng-model is updated and this watch
            // is triggered. This causes another suggestion cycle that will provide as
            // suggestion the value that is currently selected - this is unnecessary.
            if (nv === last_selected_value)
              return;

            _position_autocomplete();
            suggest(nv, current_element);
          }
        );
      }
      that.attach = debounce(_attach, user_options.debounce_attach);

      function _suggest(term, target_element) {
        $scope.selected_index = 0;
        $scope.waiting_for_suggestion = true;

        if (typeof(term) === 'string' && term.length > 0) {
          $q.when(current_options.suggest(term),
            function suggest_succeeded(suggestions) {
              // Make sure the suggestion we are processing is of the current element.
              // When using remote sources for example, a suggestion cycnle might be
              // triggered at a later time (When a different field is in focus).
              if (!current_element || current_element !== target_element)
                return;

              if (suggestions && suggestions.length > 0) {
              // Add the original term as the first value to enable the user
              // to return to his original expression after suggestions were made.
                $scope.results = [{ value: term, label: ''}].concat(suggestions);
                $scope.show_autocomplete = true;
                if (current_options.auto_select_first)
                    set_selection(1);
              } else {
                $scope.results = [];
              }
            },
            function suggest_failed(error) {
              $scope.show_autocomplete = false;
              current_options.on_error && current_options.on_error(error);
            }
          ).finally(function suggest_finally() {
            $scope.waiting_for_suggestion = false;
          });
        } else {
          $scope.waiting_for_suggestion = false;
          $scope.show_autocomplete = false;
          $scope.$apply();
        }
      }
      var suggest = debounce(_suggest, user_options.debounce_suggest);

      // Trigger end of editing and remove all attachments made by
      // this directive to the input element.
      that.detach = function () {
        if (current_element) {
          var value = current_element.val();
          update_model_value(value);
          current_options.on_detach && current_options.on_detach(value);
          current_element.unbind(EVENTS.KEYDOWN);
          current_element.unbind(EVENTS.BLUR);
        }

        // Clear references and events.
        $scope.show_autocomplete = false;
        angular.element($window).unbind(EVENTS.RESIZE);
        value_watch && value_watch();
        $scope.selected_index = $scope.results = undefined;
        current_model = current_element = previous_value = undefined;
      };

      // Update angular's model view value.
      // It is important that before triggering hooks the model's view
      // value will be synced with the visible value to the user. This will
      // allow the consumer controller to rely on its local ng-model.
      function update_model_value(value) {
        if (current_model.$modelValue !== value) {
          current_model.$setViewValue(value);
          current_model.$render();
        }
      }

      // Set the current selection while navigating through the menu.
      function set_selection(i) {
        // We use value instead of setting the model's view value
        // because we watch the model value and setting it will trigger
        // a new suggestion cycle.
        var selected = $scope.results[i];
        current_element.val(selected.value);
        $scope.selected_index = i;
        return selected;
      }

      // Apply and accept the current selection made from the menu.
      // When selecting from the menu directly (using click or touch) the
      // selection is directly applied.
      $scope.apply_selection = function (i) {
        current_element[0].focus();
        if (!$scope.show_autocomplete || i > $scope.results.length || i < 0)
          return;

        var selected = set_selection(i);
        last_selected_value = selected.value;
        update_model_value(selected.value);
        $scope.show_autocomplete = false;

        current_options.on_select && current_options.on_select(selected);
      };

      function bind_element() {
        angular.element($window).bind(EVENTS.RESIZE, position_autocomplete);

        current_element.bind(EVENTS.BLUR, function () {
          // Detach the element from the auto complete when input loses focus.
          // Focus is lost when a selection is made from the auto complete menu
          // using the mouse (or touch). In that case we don't want to detach so
          // we wait several ms for the input to regain focus.
          $timeout(function() {
            if (!current_element || current_element[0] !== $document[0].activeElement)
              that.detach();
          }, user_options.debounce_blur);
        });

        current_element.bind(EVENTS.KEYDOWN, function (e) {
          // Reserve key combinations with shift for different purposes.
          if (e.shiftKey) return;

          switch (e.keyCode) {
            // Close the menu if it's open. Or, undo changes made to the value
            // if the menu is closed.
            case KEYS.ESC:
              if ($scope.show_autocomplete) {
                $scope.show_autocomplete = false;
                $scope.$apply();
              } else {
                current_element.val(previous_value);
              }
              break;

            // Select an element and close the menu. Or, if a selection is
            // unavailable let the event propagate.
            case KEYS.ENTER:
              // Accept a selection only if results exist, the menu is
              // displayed and the results are valid (no current request
              // for new suggestions is active).
              if ($scope.show_autocomplete &&
                  $scope.selected_index > 0 &&
                  !$scope.waiting_for_suggestion) {
                $scope.apply_selection($scope.selected_index);
                // When selecting an item from the AC list the focus is set on
                // the input element. So the enter will cause a keypress event
                // on the input itself. Since this enter is not intended for the
                // input but for the AC result we prevent propagation to parent
                // elements because this event is not of their concern. We cannot
                // prevent events from firing when the event was registered on
                // the input itself.
                e.stopPropagation();
                e.preventDefault();
              }

              $scope.show_autocomplete = false;
              $scope.$apply();
              break;

            // Navigate the menu when it's open. When it's not open fall back
            // to default behavior.
            case KEYS.TAB:
              if (!$scope.show_autocomplete)
                break;

              e.preventDefault();
              /* falls through */

            // Open the menu when results exists but are not displayed. Or,
            // select the next element when the menu is open. When reaching
            // bottom wrap to top.
            case KEYS.DOWN:
              if ($scope.results.length > 0) {
                if ($scope.show_autocomplete) {
                  set_selection($scope.selected_index + 1 > $scope.results.length - 1 ? 0 : $scope.selected_index + 1);
                } else {
                  $scope.show_autocomplete = true;
                  $scope.selected_index = 0;
                }
                $scope.$apply();
              }
              break;

            // Navigate up in the menu. When reaching the top wrap to bottom.
            case KEYS.UP:
              if ($scope.show_autocomplete) {
                e.preventDefault();
                set_selection($scope.selected_index - 1 >= 0 ? $scope.selected_index - 1 : $scope.results.length - 1);
                $scope.$apply();
              }
              break;
          }
        });
      }

      $scope.$on('$destroy', function () {
        that.detach();
        $scope.container.remove();
      });
    }]
  };
}])

.directive('massAutocompleteItem', function () {
  'use strict';

  return {
    restrict: "A",
    require: ["^massAutocomplete", "ngModel"],
    scope: {'massAutocompleteItem' : "&"},
    link: function (scope, element, attrs, required) {
      // Prevent html5/browser auto completion.
      attrs.$set('autocomplete', 'off');

      element.bind('focus', function () {
        var options = scope.massAutocompleteItem();
        if (!options)
          throw "Invalid options";
        required[0].attach(required[1], element, options);
      });
    }
  };
});
