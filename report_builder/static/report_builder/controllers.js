reportBuilderApp.controller('addCtrl', function ($scope, $location, reportService) {
  reportService.options().then(function(options){
    $scope.options = options.actions.POST;
  });
  $scope.submitForm = function() {
    if ($scope.reportForm.$valid) {
      reportService.create($scope.report).then(function(result){ 
        $location.path('/report/' + result.id, true);
      });
    }
  }
});

reportBuilderApp.controller('homeCtrl', function ($scope, $routeParams, $location, $mdSidenav, reportService) {
    $scope.static = static
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

    $scope.openReport = function(reportId) {
        $mdSidenav('left').close();
        $scope.showFields = true;
        $location.path('/report/' + reportId, false);
        reportService.getReport(reportId).then(function(report) {
            $scope.fields_header = report.root_model_name;
            $scope.report = report;
            root_related_field = {
                verbose_name: report.root_model_name,
                field_name: '',
                path: '',
                model_id: report.root_model}
            data = {"model": report.root_model, "path":"", "path_verbose": "", "field": ""}
            $scope.related_fields = [root_related_field]
            reportService.getRelatedFields(data).then(function (result) {
                root_related_field.related_fields = result;
            });
            reportService.getFields(data).then(function (result) {
                $scope.fields = result;
            });
        });
    };

    if ($routeParams.reportId) {
        $scope.openReport($routeParams.reportId);
    }

    $scope.save = function() {
        $scope.report.save();
    };

});

reportBuilderApp.service('reportService', ['Restangular', function(Restangular) {
  var path = "report";
  var reports = Restangular.all(path);

  function getReport(reportId) {
    return Restangular.one(path, reportId).get();
  }
  function getRelatedFields(data) {
    return Restangular.all('related_fields').post(data);
  }
  function getFields(data) {
    return Restangular.all('fields').post(data);
  }
  function options(){
    return reports.options();
  }
  function create(data) {
    return reports.post(data);
  }
  function getList() {
    return Restangular.all('reports').getList();
  }
  function getPreview(reportId) {
    return Restangular.one(path, reportId).getList('generate');
  }

  return {
    getReport: getReport,
    getRelatedFields: getRelatedFields,
    getFields: getFields,
    options: options,
    create: create,
    getList: getList,
    getPreview: getPreview
  };
}]);

reportBuilderApp.controller('LeftCtrl', function($scope, $routeParams, $mdSidenav, $location, reportService) {
    $scope.reports = reportService.getList().$object;
    $scope.close = function() {
        $mdSidenav('left').close();
    };
    if (!$routeParams.reportId) {
        $mdSidenav('left').open();
    }
})

reportBuilderApp.controller('FieldsCtrl', function($scope, $mdSidenav, reportService) {
    $scope.help_text = '';

    $scope.load_fields = function(field) {
        data = {"model": field.model_id, "path":field.path, "path_verbose": "", "field": field.field_name}
        $scope.help_text = field.help_text;
        $scope.fields_header = field.verbose_name;
        reportService.getFields(data).then(function (result) {
            $scope.fields = result;
        });
    }

    $scope.toggle_related_fields = function(node){
        field = node.$nodeScope.$modelValue;
        parent_field = node.$parent.$modelValue;
        data = {"model": field.model_id, "path": parent_field.path, "path_verbose": "", "field": field.field_name}
        reportService.getRelatedFields(data).then(function (result) {
            field.related_fields = result;
        });
    };

    $scope.click_field = function(field) {
        $scope.help_text = field.help_text;
    };

    $scope.add_field = function(field) {
        field.report = $scope.report.id;
        $scope.report.displayfield_set.push(field);
    };
});

reportBuilderApp.controller('ReportDisplayCtrl', function($scope){
    $scope.deleteField = function(field) {
        field.remove();
    };
});
reportBuilderApp.controller('ReportShowCtrl', function($scope, $window, reportService){
    $scope.reportData = {}
    $scope.getPreview = function() {
        $scope.reportData.refresh = true;
        reportService.getPreview($scope.report.id).then(function(data) {
            columns = [];
            angular.forEach(data.meta.titles, function(value) {
                columns.push({'title': value});
            });

            $scope.reportData.items = data;
            $scope.reportData.columns = columns;
            $scope.reportData.refresh = false;
        });
    };

    $scope.getXlsx = function() {
        $window.location.href = '/report_builder/report/' + $scope.report.id + '/download_xlsx/';
    }
});
