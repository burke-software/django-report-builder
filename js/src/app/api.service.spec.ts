import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ApiService } from './api.service';
import {
  ReportsResponse,
  IReportDetailed,
  ContentTypeResponse,
  INewReport,
} from './models/api';

const apiUrl = 'api/';

describe('Api service should', function() {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService],
    });

    service = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
  });

  it('be able to get content types', () => {
    const contentTypes: ContentTypeResponse = [
      { pk: 1, name: 'log entry' },
      { pk: 2, name: 'permission' },
    ];
    service.getRootModels().subscribe(data => {
      expect(data).toEqual(contentTypes);
    });
    const req = httpMock.expectOne(apiUrl + 'contenttypes/');
    req.flush(contentTypes);
  });

  it('be able to create new report', () => {
    const report: INewReport = {
      name: 'Test Report',
      description: '',
      root_model: 1,
    };
    const detailedReport: IReportDetailed = {
      id: 1,
      name: 'Test Report',
      description: '',
      root_model: 1,
      modified: 'nevarrr',
      root_model_name: 'butts',
      displayfield_set: [],
      distinct: false,
      user_created: 3,
      user_modified: 'def dunno',
      filterfield_set: [],
      report_file_creation: null,
      report_file: null,
    };
    service.submitNewReport(report).subscribe(resp => {
      expect(resp).toBe(detailedReport);
    });
    const req = httpMock.expectOne(apiUrl + 'report/');
    req.flush(detailedReport, {
      status: 201,
      statusText: 'Created',
    });
  });

  it('be able to edit and save a report', () => {
    const report: IReportDetailed = {
      id: 4,
      name: 'afasdf',
      description: 'adgsasfg',
      modified: '2018-01-18',
      root_model: 5,
      root_model_name: 'content type',
      displayfield_set: [
        {
          name: 'model',
          field: 'model',
          field_verbose: 'python model class name',
          field_type: 'CharField',
          is_default: true,
          field_choices: [],
          can_filter: true,
          path: '',
          path_verbose: '',
          help_text: '',
          report: 4,
          position: 0,
        },
        {
          name: 'id',
          field: 'id',
          field_verbose: 'ID',
          field_type: 'AutoField',
          is_default: true,
          field_choices: [],
          can_filter: true,
          path: '',
          path_verbose: '',
          help_text: '',
          report: 4,
          position: 1,
        },
      ],
      distinct: false,
      user_created: 1,
      user_modified: null,
      filterfield_set: [],
      report_file: null,
      report_file_creation: null,
      lastSaved: '2018-01-18T16:00:05.527Z',
    };

    const expected: IReportDetailed = {
      id: 4,
      name: 'afasdf',
      description: 'adgsasfg',
      modified: '2018-01-18',
      root_model: 5,
      root_model_name: 'content type',
      displayfield_set: [
        {
          id: 1,
          path: '',
          path_verbose: '',
          field: 'model',
          field_verbose: 'python model class name',
          name: 'model',
          sort: null,
          sort_reverse: false,
          width: 15,
          aggregate: '',
          position: 0,
          total: false,
          group: false,
          report: 4,
          display_format: null,
          field_type: 'CharField',
        },
        {
          id: 2,
          path: '',
          path_verbose: '',
          field: 'id',
          field_verbose: 'ID',
          name: 'id',
          sort: null,
          sort_reverse: false,
          width: 15,
          aggregate: '',
          position: 1,
          total: false,
          group: false,
          report: 4,
          display_format: null,
          field_type: 'AutoField',
        },
      ],
      distinct: false,
      user_created: 1,
      user_modified: null,
      filterfield_set: [],
      report_file: null,
      report_file_creation: null,
    };

    service.editReport(report).subscribe(response => {
      expect(response).toEqual(expected);
    });

    const req = httpMock.expectOne(apiUrl + 'report/4/');
    req.flush(expected);
  });

  it('be able to get list of reports', () => {
    const reports: ReportsResponse = [
      {
        id: 4,
        name: 'fdsfs',
        modified: '2017-09-26',
        root_model: 3,
        root_model_name: 'group',
        user_created: {
          first_name: 'Test',
          last_name: 'User',
          id: 1,
        },
      },
    ];
    service.getReports().subscribe(data => {
      expect(data).toEqual(reports);
    });
    const req = httpMock.expectOne(apiUrl + 'reports/');
    req.flush(reports);
  });

  it('be able to get details of one report', () => {
    const report: IReportDetailed = {
      id: 1,
      name: 'a',
      description: '',
      modified: '2017-09-28',
      root_model: 21,
      root_model_name: 'report',
      displayfield_set: [
        {
          id: 1,
          path: '',
          path_verbose: '',
          field: 'id',
          field_verbose: 'ID',
          name: 'id',
          sort: null,
          sort_reverse: false,
          width: 15,
          aggregate: '',
          position: 0,
          total: false,
          group: false,
          report: 1,
          display_format: null,
          field_type: 'AutoField',
          field_choices: [],
        },
      ],
      distinct: false,
      user_created: 1,
      user_modified: null,
      filterfield_set: [],
      report_file: 'http://localhost:8000/media/report_files/a_0928_2204.xlsx',
      report_file_creation: '2017-09-28T22:04:49.407527Z',
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

  it('be able to generate a preview of the report', () => {
    const expected = {
      data: [['place', 10], ['user', 4]],
      meta: { titles: ['model', 'id'] },
    };

    service.generatePreview(1).subscribe(response => {
      expect(response).toEqual(expected);
    });

    const req = httpMock.expectOne(apiUrl + 'report/1/generate/');
    req.flush(expected);
  });
});
