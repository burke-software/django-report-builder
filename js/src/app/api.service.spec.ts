import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ApiService } from './api.service';
import { ReportsResponse, IReportDetailed, ContentTypeResponse } from './api.interfaces';
import { IReportForm } from './new-report/interfaces';

const apiUrl = '/report_builder/api/';

describe('Api service should', function () {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: [
        ApiService,
      ]
    });

    service = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
  });

  it('be able to get content types', () =>  {
    const contentTypes: ContentTypeResponse = [
      { 'pk': 1, 'name': 'log entry' },
      { 'pk': 2, 'name': 'permission'},
    ];
    service.getRootModels().subscribe(data => {
      expect(data).toEqual(contentTypes);
    });
    const req = httpMock.expectOne(apiUrl + 'contenttypes/');
    req.flush(contentTypes);
  });

  it('be able to create new report', () =>  {
    const report: IReportForm = {
      name: 'Test Report',
      description: '',
      root_model: 1,
    };
    service.submitNewReport(report).then((resp) => {
      expect(resp).toBe(report);
    });
    const req = httpMock.expectOne(apiUrl + 'report/');
    req.flush(report, {
      status: 201,
      statusText: 'Created',
    });
  });

  it('be able to get list of reports', () =>  {
    const reports: ReportsResponse = [{
      'id': 4,
      'name': 'fdsfs',
      'modified': '2017-09-26',
      'root_model': 3,
      'root_model_name': 'group',
      'user_created': {
        'first_name': 'Test',
        'last_name': 'User',
        'id': 1
      }
    }];
    service.getReports().subscribe(data => {
      expect(data).toEqual(reports);
    });
    const req = httpMock.expectOne(apiUrl + 'reports/');
    req.flush(reports);
  });

  it('be able to get details of one report', () =>  {
    const report: IReportDetailed = {
      'id': 1,
      'name': 'a',
      'description': '',
      'modified': '2017-09-28',
      'root_model': 21,
      'root_model_name': 'report',
      'displayfield_set': [
          {
              'id': 1,
              'path': '',
              'path_verbose': '',
              'field': 'id',
              'field_verbose': 'ID',
              'name': 'id',
              'sort': null,
              'sort_reverse': false,
              'width': 15,
              'aggregate': '',
              'position': 0,
              'total': false,
              'group': false,
              'report': 1,
              'display_format': null,
              'field_type': 'AutoField'
          }
      ],
      'distinct': false,
      'user_created': 1,
      'user_modified': null,
      'filterfield_set': [],
      'report_file': 'http://localhost:8000/media/report_files/a_0928_2204.xlsx',
      'report_file_creation': '2017-09-28T22:04:49.407527Z'
    };
    service.getReport(report.id).subscribe(data => {
      expect(data).toEqual(report);
    });
    const req = httpMock.expectOne(apiUrl + 'report/1/');
    req.flush(report);
  });

  it('be able to delete a report', () => {
    service.deleteReport(1).subscribe(response => {
      expect(response).toEqual({});
    });

    const req = httpMock.expectOne(apiUrl + 'report/1/');
    req.flush({});
  });
});
