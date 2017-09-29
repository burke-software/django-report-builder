import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { IReportForm } from './new-report/interfaces';
import { ReportsResponse, IReportDetailed, ContentTypeResponse } from './api.interfaces';

@Injectable()
export class ApiService {
  apiUrl = '/report_builder/api/';

  constructor(private http: Http) { }

  getRootModels(): Observable<ContentTypeResponse> {
    return this.http.get(this.apiUrl + 'contenttypes/')
      .map(response => response.json());
  }

  submitNewReport(form: IReportForm) {
    return this.http.post(this.apiUrl + 'report/', form).toPromise();
  }

  getReports(): Observable<ReportsResponse> {
    return this.http.get(this.apiUrl + 'reports/')
      .map(response => response.json());
  }

  getReport(reportId: number): Observable<IReportDetailed> {
    return this.http.get(this.apiUrl + `report/${reportId}/`)
      .map(response => response.json());
  }
}
