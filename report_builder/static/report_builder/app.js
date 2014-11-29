var reportBuilderApp = angular.module('reportBuilderApp', ['ngRoute', 'restangular', 'ngMaterial', 'ui.tree']);

reportBuilderApp.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl("/report_builder/api");
    return RestangularProvider.setRequestSuffix("/");
});

reportBuilderApp.config(function($routeProvider, $locationProvider) {
    $routeProvider.
        when("/", {
            controller: "homeCtrl",
            templateUrl: STATIC_URL + 'report_builder/partials/home.html'
        }).
        when("/report/:reportId", {
            controller: "homeCtrl",
            templateUrl: STATIC_URL + 'report_builder/partials/home.html'
        })
    return $locationProvider.html5Mode(true);
});

reportBuilderApp.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
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
