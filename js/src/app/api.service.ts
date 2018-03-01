import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import {
  ReportsResponse,
  IReportDetailed,
  ContentTypeResponse,
  IGetRelatedFieldRequest,
  IRelatedField,
  IField,
  IReportPreview,
  IConfig,
  INewReport,
  IAsyncTaskId,
  ITaskStatus,
  IExportType,
} from './models/api';

interface ITest {
  [key: string]: string[];
}

interface ISaveError {
  [key: string]: ITest[];
}

const flatten = (arr: any[]) => [].concat(...arr);

@Injectable()
export class ApiService {
  baseUrl = '/report_builder/';
  apiUrl = this.baseUrl + 'api/';

  constructor(private http: HttpClient) {}

  private handleSaveError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // Error happens before hitting the server (JS error or network error)
      console.error('network error');
    } else {
      const message = flatten(
        Object.entries(error.error as ISaveError).map(([tab, items]) =>
          items.map((item, i) =>
            Object.entries(item).map(([itemName, errors]) =>
              errors.map(
                e =>
                  `In ${tab}, your ${i} field's ${itemName} has the error: ${e}`
              )
            )
          )
        )
      ).join('\n');

      return new ErrorObservable(
        'Saving encountered the following errors: \n' + message
      );
    }
    return new ErrorObservable("We're sorry, something went wrong!");
  }

  getConfig() {
    return this.http.get<IConfig>(this.apiUrl + 'config/');
  }

  getRootModels() {
    return this.http.get<ContentTypeResponse>(this.apiUrl + 'contenttypes/');
  }

  submitNewReport(form: INewReport) {
    return this.http.post<IReportDetailed>(this.apiUrl + 'report/', form);
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
    return this.http
      .put<IReportDetailed>(this.apiUrl + `report/${form.id}/`, form)
      .catch(this.handleSaveError);
  }

  generatePreview(reportId: number) {
    return this.http.get<IReportPreview>(
      this.apiUrl + `report/${reportId}/generate/`
    );
  }

  exportReport({ reportId, type }: { reportId: number; type: IExportType }) {
    return this.http.get<IAsyncTaskId>(
      this.baseUrl + `report/${reportId}/download_file/${type}/`
    );
  }

  checkStatus({
    reportId,
    taskId,
  }: {
    reportId: number | string;
    taskId: string;
  }) {
    return this.http.get<ITaskStatus>(
      this.baseUrl + `report/${reportId}/check_status/${taskId}/`
    );
  }

  copyReport(reportId: number) {
    return this.http.post<IReportDetailed>(
      this.apiUrl + `report/${reportId}/copy_report/`,
      null
    );
  }
}
