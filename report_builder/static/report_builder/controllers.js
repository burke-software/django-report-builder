reportBuilderApp.controller('homeCtrl', function ($scope, $routeParams, $location, $mdSidenav, Restangular) {
    $scope.openReport = function(reportId) {
        $mdSidenav('left').close();
        $scope.showFields = true;
        $location.path('/report/' + reportId, false);
        Restangular.one('reports', reportId).get().then(function(report) {
            $scope.report = report;
            data = {"model": report.root_model, "path":"", "path_verbose": "", "field": ""}
            Restangular.all('related_fields').post(data).then(function (result) {
                $scope.related_fields = result;
            });
            Restangular.all('fields').post(data).then(function (result) {
                $scope.fields = result;
            });
        });
    }

    if ($routeParams.reportId) {
        $scope.openReport($routeParams.reportId);
    }
});

reportBuilderApp.controller('LeftCtrl', function($scope, $routeParams, $mdSidenav, $location, Restangular) {
    $scope.reports = Restangular.all('reports').getList().$object;
    $scope.close = function() {
        $mdSidenav('left').close();
    };
    if (!$routeParams.reportId) {
        $mdSidenav('left').open();
    }
})

reportBuilderApp.controller('FieldsCtrl', function($scope, $mdSidenav, Restangular) {
});
