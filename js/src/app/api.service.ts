import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { IReportForm } from './new-report/interfaces';
import {
  ReportsResponse,
  IReportDetailed,
  ContentTypeResponse,
  IGetRelatedFieldRequest,
  IRelatedField,
  IField
} from './api.interfaces';

@Injectable()
export class ApiService {
  apiUrl = '/report_builder/api/';

  constructor(private http: HttpClient) {}

  getRootModels() {
    return this.http.get<ContentTypeResponse>(this.apiUrl + 'contenttypes/');
  }

  submitNewReport(form: IReportForm) {
    return this.http.post(this.apiUrl + 'report/', form).toPromise();
  }

  getReports() {
    return this.http.get<ReportsResponse>(this.apiUrl + 'reports/');
  }

  getReport(reportId: number) {
    return this.http.get<IReportDetailed>(this.apiUrl + `report/${reportId}/`);
  }

  getRelatedFields(request: IGetRelatedFieldRequest) {
    return this.http.post<IRelatedField[]>(
      this.apiUrl + 'related_fields/',
      request
    );
  }

  getFields(request: IGetRelatedFieldRequest) {
    return this.http.post<IField[]>(this.apiUrl + 'fields/', request);
  }

  deleteReport(reportId: number) {
    return this.http.delete(this.apiUrl + `report/${reportId}/`);
  }

  editReport(form: IReportDetailed) {
    return this.http.put<IReportDetailed>(
      this.apiUrl + `report/${form.id}/`,
      form
    );
  }
}
