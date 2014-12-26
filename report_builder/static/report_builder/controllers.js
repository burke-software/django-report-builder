reportBuilderApp.controller('addCtrl', function ($scope, $location, Restangular) {
  resource = Restangular.all('reports');
  resource.options().then(function(options){
    $scope.options = options.actions.POST;
  });
  $scope.submitForm = function() {
    if ($scope.reportForm.$valid) {
      resource.post($scope.report).then(function(result){ 
        $location.path('/report/' + result.id, true);
      });
    }
  }
});

reportBuilderApp.controller('homeCtrl', function ($scope, $routeParams, $location, $mdSidenav, Restangular) {
    $scope.tabData = {
        selectedIndex: 0,
    };
    $scope.next = function() {
        $scope.tabData.selectedIndex = Math.min($scope.tabData.selectedIndex + 1, 2) ;
    };
    $scope.previous = function() {
        $scope.tabData.selectedIndex = Math.max($scope.tabData.selectedIndex - 1, 0);
    };

    $scope.reports_list_menu = function() {
        $mdSidenav('left').open();
    };
    $scope.field_menu = function() {
        $mdSidenav('right').open();
    };

    $scope.requestFullscreen = function() {
        var
        el = document.documentElement
        , rfs =
            el.requestFullScreen
            || el.webkitRequestFullScreen
            || el.mozRequestFullScreen
        ;
        rfs.call(el);
    };

    $scope.displayFields = [];

    $scope.openReport = function(reportId) {
        $mdSidenav('left').close();
        $scope.showFields = true;
        $location.path('/report/' + reportId, false);
        Restangular.one('reports', reportId).get().then(function(report) {
            $scope.displayFields = report.displayfield_set;
            $scope.fields_header = report.root_model_name;
            $scope.report = report;
            root_related_field = {
                verbose_name: report.root_model_name,
                field_name: '',
                path: '',
                model_id: report.root_model}
            data = {"model": report.root_model, "path":"", "path_verbose": "", "field": ""}
            $scope.related_fields = [root_related_field]
            Restangular.all('related_fields').post(data).then(function (result) {
                root_related_field.related_fields = result;
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
    $scope.help_text = '';

    $scope.load_fields = function(field) {
        data = {"model": field.model_id, "path":field.path, "path_verbose": "", "field": field.field_name}
        $scope.help_text = field.help_text;
        $scope.fields_header = field.verbose_name;
        Restangular.all('fields').post(data).then(function (result) {
            $scope.fields = result;
        });
    }

    $scope.toggle_related_fields = function(node){
        field = node.$nodeScope.$modelValue;
        parent_field = node.$parent.$modelValue;
        data = {"model": field.model_id, "path": parent_field.path, "path_verbose": "", "field": field.field_name}
        Restangular.all('related_fields').post(data).then(function (result) {
            field.related_fields = result;
        });
    };

    $scope.click_field = function(field) {
        $scope.help_text = field.help_text;
    };

    $scope.add_field = function(field) {
        $scope.displayFields.push(field);
    };
});

reportBuilderApp.controller('ReportDisplayCtrl', function($scope){
});
