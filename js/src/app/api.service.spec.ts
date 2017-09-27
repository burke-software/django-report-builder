import {MockBackend, MockConnection} from '@angular/http/testing';
import {BaseRequestOptions, Http, Headers, ResponseOptions, Response} from '@angular/http';
import { async, TestBed } from '@angular/core/testing';

import { ApiService, ContentTypeResponse } from './api.service';
import { IReportForm } from './new-report/interfaces';

const defaultHeaders = new Headers({'Content-Type': 'application/json'});

describe('Api service should', function () {
  let service: ApiService;
  let mockBackend: MockBackend;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ApiService,
        MockBackend,
        BaseRequestOptions,
        {
          provide: Http,
          useFactory: (backend: MockBackend, defaultOptions: BaseRequestOptions) => {
            return new Http(backend, defaultOptions);
          },
          deps: [MockBackend, BaseRequestOptions],
        }
      ]
    });

    service = TestBed.get(ApiService);
    mockBackend = TestBed.get(MockBackend);
  });

  it('be able to get content types', () =>  {
    const contentTypes: ContentTypeResponse = [
      { 'pk': 1, 'name': 'log entry' },
      { 'pk': 2, 'name': 'permission'},
    ];
    mockBackend.connections.subscribe(
      (connection: MockConnection) => {
        connection.mockRespond(new Response(
          new ResponseOptions({
            body: contentTypes,
            status: 200,
            headers: defaultHeaders
          })));
      });
    service.getRootModels().subscribe(data => {
      expect(data).toEqual(contentTypes);
    });
  });

  it('be able to create new report', () =>  {
    const report: IReportForm = {
      name: 'Test Report',
      description: '',
      root_model: 1,
    };
    mockBackend.connections.subscribe(
      (connection: MockConnection) => {
        connection.mockRespond(new Response(
          new ResponseOptions({
            body: report,
            status: 201,
            headers: defaultHeaders
          })));
      });
    service.submitNewReport(report).then((resp) => {
      expect(resp.status).toBe(201);
    });
  });
});
