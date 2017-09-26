import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { IReportForm } from './new-report/interfaces';

interface IContentType {
  'pk': number;
  'name': string;
}

export type ContentTypeResponse = IContentType[];


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
}
