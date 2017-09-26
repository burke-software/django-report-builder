import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';

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
}
