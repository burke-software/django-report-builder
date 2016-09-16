reportBuilderApp.controller('addCtrl', function($scope, $location, reportService) {
  reportService.options().then(function(options) {
    $scope.options = options.actions.POST;
  });
  $scope.submitForm = function() {
    if ($scope.reportForm.$valid) {
      reportService.create($scope.report).then(function(result) {
        $location.path('/report/' + result.id, true);
      });
    }
  };
});

reportBuilderApp.controller('homeCtrl', function($scope, $routeParams, $location, $mdSidenav, reportService) {
  $scope.static = static;
  $scope.ASYNC_REPORT = ASYNC_REPORT;
  $scope.reportData = {};
  reportService.filterFieldOptions().then(function(options) {
    $scope.filterFieldOptions = options.actions.POST;
  });
  reportService.getFormats().then(function(data) {
    $scope.formats = data;
  });

  $scope.reports_list_menu = function() {
    $mdSidenav('left').open();
  };
  $scope.field_menu = function() {
    $mdSidenav('right').open();
  };
  $scope.selectedIndex = 0;

  $scope.fieldCanFilter = function(field) {
    if ($scope.selectedIndex === 0) {
      return true;
    }
    if ($scope.selectedIndex === 1 && field.can_filter === true) {
      return true;
    }
    return false;
  };

  $scope.requestFullscreen = function() {
    var
    el = document.documentElement,
      rfs =
        el.requestFullScreen || el.webkitRequestFullScreen || el.mozRequestFullScreen;
    rfs.call(el);
  };

  $scope.openReport = function(reportId) {
    $scope.showFields = true;
    $location.path('/report/' + reportId, false);
    reportService.getReport(reportId).then(function(report) {
      $mdSidenav('left').close();
      $scope.fields_header = report.root_model_name;
      $scope.report = report;
      $scope.report.lastSaved = null;
      $scope.report.create_chart_lists = true;
      root_related_field = {
        verbose_name: report.root_model_name,
        field_name: '',
        path: '',
        model_id: report.root_model
      };
      data = {
        "model": report.root_model,
        "path": "",
        "path_verbose": "",
        "field": ""
      };
      $scope.related_fields = [root_related_field];
      reportService.getRelatedFields(data).then(function(result) {
        root_related_field.related_fields = result;
        var help_text = 'This model is included in report builder.';
        if (result[0].included_model == false) {
          help_text = 'This model is not included in report builder.';
        }
        $scope.help_text = help_text;
      });
      reportService.getFields(data).then(function(result) {
        $scope.fields = result;
      });
    });
  };

  if ($routeParams.reportId) {
    $scope.openReport($routeParams.reportId);
  }

});

reportBuilderApp.service('reportService', ['Restangular',
  function(Restangular) {
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

    function getFormats() {
      return Restangular.all('formats').getList();
    }

    function options() {
      return reports.options();
    }

    function filterFieldOptions() {
      return Restangular.all('filterfields').options();
    }

    function create(data) {
      return reports.post(data);
    }

    function deleteReport(reportId) {
      return Restangular.one(path, reportId).remove();
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
      getFormats: getFormats,
      options: options,
      filterFieldOptions: filterFieldOptions,
      create: create,
      deleteReport: deleteReport,
      getList: getList,
      getPreview: getPreview
    };
  }
]);

reportBuilderApp.controller('LeftCtrl', function($scope, $routeParams, $mdSidenav, $location, reportService) {
  $scope.reports = reportService.getList().$object;
  $scope.reportOrder = "name";
  $scope.reverseReportOrder = false;

  $scope.currentUserFilter = function(report) {
    if ( report.user_created !== null ){
      return ( report.user_created.id == CURRENT_USER );
    } else {
      return false;
    }
  };

  $scope.notCurrentUserFilter = function(report) {
    return !( $scope.currentUserFilter(report) );
  };

  $scope.close = function() {
    $mdSidenav('left').close();
  };
  if (!$routeParams.reportId) {
    $mdSidenav('left').open();
  }
});

reportBuilderApp.controller('FieldsCtrl', function($scope, $mdSidenav, reportService) {
  $scope.load_fields = function(field) {
    data = {
      "model": field.model_id,
      "path": field.path,
      "path_verbose": field.path_verbose,
      "field": field.field_name
    };
    $scope.help_text = field.help_text;
    $scope.fields_header = field.verbose_name;
    reportService.getFields(data).then(function(result) {
      $scope.fields = result;
    });
    reportService.getRelatedFields(data).then(function(result) {
      field.related_fields = result;
      var help_text = 'This model is included in report builder.';
      if (result[0].included_model == false) {
        help_text = 'This model is not included in report builder.';
      }
      $scope.help_text = help_text;
    });
  };

  $scope.toggle_related_fields = function(node) {
    field = node.$nodeScope.$modelValue;
    parent_field = node.$parent.$modelValue;
    data = {
      "model": field.model_id,
      "path": parent_field.path,
      "field": field.field_name
    };
    reportService.getRelatedFields(data).then(function(result) {
      field.related_fields = result;
    });
  };

  $scope.click_field = function(field) {
    $scope.help_text = '[' + field.field_type + '] ' + field.help_text;
  };

  $scope.add_field = function(field) {
    field.report = $scope.report.id;
    if ($scope.selectedIndex === 0) {
      $scope.report.displayfield_set.push(angular.copy(field));
    } else if ($scope.selectedIndex === 1) {
      $scope.report.filterfield_set.push(angular.copy(field));
    }
  };
});

reportBuilderApp.controller('ReportDisplayCtrl', function($scope) {
  $scope.deleteField = function(field) {
    field.remove();
  };
});

reportBuilderApp.controller('ReportOptionsCtrl', function($scope, $location, $window, reportService) {
  $scope.deleteReport = function(reportId) {
    var url = $location.url();
    var absUrl = $location.absUrl();
    var origin = absUrl.substr(0,absUrl.indexOf(url));
    reportService.deleteReport(reportId).then(function() {
      // Getting another ID to redirect to now that our report has been deleted
      reportService.getList().then(function(list) {
        if (list[0]) {
          $window.location.href = origin + '/report/' + list[0].id;
        } else {
          $window.location.href = origin;
        }
        // $location.path('/report/' + list[0].id, true);
      });
    });
  };
});

reportBuilderApp.controller('ReportFilterCtrl', function($scope) {
  $scope.deleteField = function(field) {
    field.remove();
  };
});

reportBuilderApp.controller('ChartOptionsCtrl', function($scope, $window, $http, $timeout, $mdToast, reportService) {
  $scope.chart_styles = ['area', 'bar', 'column', 'line', 'pie'];

  $scope.$watch('report.displayfield_set', function(newValue, oldValue) {
    if (newValue === undefined || $scope.report === undefined) return;
    $scope.report_fields_indexes = newValue.map(function(el, idx) { return idx; });
    $scope.report_fields_names = newValue.map(function(el, idx) { return el.name; });
  }, true);

  function isNotEmpty(string) {
    return string !== '';
  }

  function parseInt1(el) {
    return parseInt(el);
  }

  function toListOfInts(element_name, list_name) {
    if ($scope.report[element_name] === null) {
      $scope.report[list_name] = [];
    } else {
      $scope.report[list_name] = $scope.report[element_name].split(',').filter(isNotEmpty).map(parseInt1);
    }
  }

  $scope.$watch('report.create_chart_lists', function(newValue, oldValue) {
    if (newValue) {
      toListOfInts('chart_categories', 'chart_categories_list');
      toListOfInts('chart_series', 'chart_series_list');
      toListOfInts('chart_values', 'chart_values_list');
      $scope.report.create_chart_lists = false;
    }
  });

  $scope.remove_from_list = function(index, list_name) {
    var name = 'chart_' + list_name + '_list';
    $scope.report[name].splice(index, 1);
  };
  $scope.add_to_list = function(list_name) {
    var name = 'chart_' + list_name + '_list';
    $scope.report[name].push(null);
  };
});

reportBuilderApp.controller('ReportShowCtrl', function($scope, $window, $http, $timeout, $mdToast, reportService) {

  function chart_series_from_columns(data, x, y, titles) {
    var categories = [];
    var unique_categories = [];
    data.forEach(function(row, idx) {
      var row_category = "";
      for (var i = 0; i < x.length; i++) {
        if (x[i] == null) continue;
        row_category += row[x[i]];
      }
      categories.push(row_category);
      if (unique_categories.indexOf(row_category) < 0) {
        unique_categories.push(row_category);
      }
    });
    var series_data = [];
    for (var i = 0; i < y.length; i++) {
      if (y[i] == null) continue;
      series_data.push({
        name: titles[y[i]],
        data: data.map(function(row, idx) {
          return [ categories[idx], row[y[i]]];
        }),
      });
    }
    return {
      categories: unique_categories,
      series: series_data,
    };
  }

  function chart_series_from_rows(data, x1, x2, y) {
    var categories = [];
    var unique_categories = [];
    data.forEach(function(row, idx) {
      var row_category = "";
      for (var i = 0; i < x1.length; i++) {
        if (x1[i] == null) continue;
        row_category += row[x1[i]];
      }
      categories.push(row_category);
      if (unique_categories.indexOf(row_category) < 0) {
        unique_categories.push(row_category);
      }
    });
    var series_data_dict = {};
    for (i = 0; i < data.length; i++) {
      var row_series = "";
      for (var j = 0; j < x2.length; j++) {
        if (x2[j] == null) continue;
        row_series += data[i][x2[j]];
      }
      if (! (row_series in series_data_dict)) {
        series_data_dict[row_series] = [];
      }
      series_data_dict[row_series].push([categories[i], data[i][y]]);
    }
    var series_data = [];
    for (var key in series_data_dict) {
      series_data.push({
        name: key,
        data: series_data_dict[key]
      });
    }
    return {
      categories: unique_categories,
      series: series_data,
    };
  }

  function prepare_for_chart(data, report) {
    var totals = false;
    report.displayfield_set.forEach(function(field) {
      if (field.total) {
        totals = true;
      }
    });
    if (totals) {
      data.splice(data.length - 2, 2);
    }
  }

  $scope.getPreview = function() {
    $scope.reportData.chart = false;
    $scope.reportData.statusMessage = null;
    $scope.reportData.refresh = true;
    reportService.getPreview($scope.report.id).then(function(data) {
      columns = [];
      angular.forEach(data.meta.titles, function(value) {
        columns.push({
          'title': value
        });
      });
      $scope.reportData.items = data;
      $scope.reportData.columns = columns;
      $scope.reportData.refresh = false;
    }, function(response) {
      $scope.reportData.refresh = false;
      $scope.reportData.statusMessage = "Error with status code " + response.status;
    });
  };

  $scope.createChart = function() {
    $scope.reportData.chart = true;
    $scope.reportData.statusMessage = null;
    $scope.reportData.refresh = true;
    reportService.getPreview($scope.report.id).then(function(data) {
      prepare_for_chart(data, $scope.report);
      var chart_data = {};
      if ($scope.report.chart_type == 2) {
        chart_data = chart_series_from_columns(data, $scope.report.chart_categories_list,
                                               $scope.report.chart_values_list, data.meta.titles);
      }
      else if ($scope.report.chart_type == 3) {
        chart_data = chart_series_from_rows(data, $scope.report.chart_categories_list, $scope.report.chart_series_list, $scope.report.chart_values_list[0]);
      } else {
        return;
      }
      var chart_dict = {
        chart: {
          type: $scope.report.chart_style,
          height: 450,
        },
        xAxis: {
          categories: chart_data.categories,
        },
        title: {
          text: $scope.report.name,
        },
        yAxis: {
          stackLabels: {
            enabled: $scope.report.chart_total,
            formatter: function() {return 'total: ' + this.total;},
          }
        },
        series: chart_data.series,
      };
      chart_dict['plotOptions'] = {};
      chart_dict['plotOptions'][$scope.report.chart_style] = {
        dataLabels: {
          enabled: $scope.report.chart_labels,
        },
        stacking: $scope.report.chart_stacked ? 'normal' : false,
      };
      var chart = Highcharts.chart('highchart_container', chart_dict);
      if ($scope.report.chart_style == 'bar' && chart_data.categories.length * chart_data.series.length > 15 ) {
        var series_size = 1;
        if (chart_data.series.length > 1) {
           series_size = chart_data.series.length / 2;
        }
        var size = chart_data.categories.length * series_size * 20;
        chart.setSize(null, Math.max(size + 100, 450));
      }

      $scope.reportData.refresh = false;
    }, function(response) {
      $scope.reportData.refresh = false;
      $scope.reportData.statusMessage = "Error with status code " + response.status;
    });
  };

  function isNotNull(value) {
    return value !== undefined && value !== null;
  }

  $scope.save = function() {
    angular.forEach($scope.report.displayfield_set, function(value, index) {
      value.position = index;
      if (value.sort === "") {
        value.sort = null;
      }
    });
    angular.forEach($scope.report.filterfield_set, function(value, index) {
      value.position = index;
    });
    $scope.report.chart_categories = $scope.report.chart_categories_list.filter(isNotNull).join(',');
    $scope.report.chart_values = $scope.report.chart_values_list.filter(isNotNull).join(',');
    $scope.report.chart_series = $scope.report.chart_series_list.filter(isNotNull).join(',');
    $scope.report.save().then(function(result) {
      $scope.report.lastSaved = new Date();
      $scope.reportData.reportErrors = null;
      $mdToast.show(
        $mdToast.simple()
        .content('Report Saved!')
        .hideDelay(1000));
    }, function(response) {
      $mdToast.show(
        $mdToast.simple()
        .content('Unable to Save!')
        .hideDelay(1000));
      $scope.reportData.reportErrors = response.data;
    });
  };

  $scope.downloadReport = function(filetype) {
    base_url = BASE_URL + 'report/' + $scope.report.id;
    url = base_url + '/download_file/' + filetype + '/';
    $scope.workerStatus = 'Requesting report';
    if (ASYNC_REPORT === "True") {
      $http.get(url).
      success(function(data) {
        $scope.workerStatus = 'Report Requested';
        var attempts = 0;
        var task_id = data.task_id;
        var checkPoller = function() {
          $http.get(base_url + '/check_status/' + task_id + '/').success(function(check_data) {
            if (check_data.state === "SUCCESS") {
              $scope.workerStatus = null;
              $scope.workerState = null;
              $window.location.href = check_data.link;
              $mdToast.show(
                $mdToast.simple()
                .content('Report Ready!')
                .hideDelay(4000));
            } else {
              $scope.workerStatus = 'Waiting on worker. State is ' + check_data.state;
              $scope.workerState = check_data.state;
              attempts += 1;
              if (check_data.state !== "FAILURE") {
                $timeout(checkPoller, 1000 + (500 * attempts));
              }
            }
          });
        };
        $timeout(checkPoller, 100);
      });
    } else {
      $window.location.href = url;
    }
  };
});
