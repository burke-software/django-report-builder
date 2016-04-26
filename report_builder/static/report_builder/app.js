var reportBuilder = angular.module('reportBuilder', ['ngRoute', 'restangular', 'ngMaterial', 'ui.tree', 'ngHandsontable', 'angularPikaday']);

reportBuilder.config(function($sceProvider) {
   $sceProvider.enabled(false);
});

reportBuilder.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl(BASE_URL + "api");
    RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
      var extractedData;
      if (operation === "getList" && _.has(data, 'meta')) {
        extractedData = data.data;
        extractedData.meta = data.meta;
      } else {
        extractedData = data;
      }
      return extractedData;
    });
    return RestangularProvider.setRequestSuffix("/");
});

function static(path) {
    /* Works like django static files - adds the static path */
    return STATIC_URL + path;
}

reportBuilder.config(function($routeProvider, $httpProvider, $locationProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $routeProvider.
        when("/", {
            controller: "homeCtrl",
            templateUrl: static('report_builder/partials/home.html')
        }).
        when("/report/add", {
            controller: "addCtrl",
            templateUrl: static('report_builder/partials/add.html')
        }).
        when("/report/:reportId", {
            controller: "homeCtrl",
            templateUrl: static('report_builder/partials/home.html')
        })
    return $locationProvider.html5Mode(true);
});

reportBuilder.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue-grey')
    .accentPalette('orange');
});

reportBuilder.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
    var original = $location.path;
    $location.path = function (path, reload) {
        if (reload === false) {
            var lastRoute = $route.current;
            var un = $rootScope.$on('$locationChangeSuccess', function () {
                $route.current = lastRoute;
                un();
            });
        }
        return original.apply($location, [path]);
    };
    $rootScope.MEDIA_URL = MEDIA_URL;
    $rootScope.STATIC_URL = STATIC_URL;
}]);

var reportBuilderApp = angular.module('reportBuilderApp', ['reportBuilder']);
