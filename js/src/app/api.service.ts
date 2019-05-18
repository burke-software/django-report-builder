import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';




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

@Injectable()
export class ApiService {
  apiUrl = 'api/';

  constructor(private http: HttpClient) {}

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
    return this.http.put<IReportDetailed>(
      this.apiUrl + `report/${form.id}/`,
      form
    );
  }

  generatePreview(reportId: number) {
    return this.http.get<IReportPreview>(
      this.apiUrl + `report/${reportId}/generate/`
    );
  }

  exportReport({ reportId, type }: { reportId: number; type: IExportType }) {
    return this.http.get<IAsyncTaskId>(
      `api/report/${reportId}/download_file/${type}/`
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
      `api/report/${reportId}/check_status/${taskId}/`
    );
  }

  copyReport(reportId: number) {
    return this.http.post<IReportDetailed>(
      this.apiUrl + `report/${reportId}/copy_report/`,
      null
    );
  }
}
