import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/do';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/observable/forkJoin';

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Effect, Actions } from '@ngrx/effects';
import { Action } from '@ngrx/store';

import { ApiService } from '../api.service';
import * as fromReports from '../actions/reports';
import { IGetRelatedFieldRequest } from '../api.interfaces';

@Injectable()
export class ReportEffects {
  @Effect()
  getReports$: Observable<Action> = this.actions$
    .ofType(fromReports.GET_REPORT_LIST)
    .mergeMap(() =>
      this.api.getReports()
        .map((reports) => new fromReports.SetReportList(reports))
    );

  constructor(
    private actions$: Actions,
    private api: ApiService,
    private router: Router
  ) {}

  @Effect()
  getReport$: Observable<Action> = this.actions$
    .ofType(fromReports.GET_REPORT)
    .map((action: fromReports.GetReport) => action.payload)
    .mergeMap((reportId) =>
      this.api.getReport(reportId)
        .map(report => new fromReports.GetReportSuccess(report))
    );

  @Effect()
  getReportSuccess$ = this.actions$
    .ofType(fromReports.GET_REPORT_SUCCESS)
    .map((action: fromReports.GetReportSuccess) => action.payload)
    .do((report) => this.router.navigate(['/report', report.id]))
    .mergeMap((report) => {
      const request: IGetRelatedFieldRequest = {
        model: report.root_model,
        path: '',
        field: '',
      };
      return Observable.forkJoin(
        this.api.getRelatedFields(request),
        this.api.getFields(request),
      ).map(([relatedFields, fields]) => new fromReports.GetReportFieldsSuccess({relatedFields, fields}));
    });

  @Effect()
  getFields$ = this.actions$
    .ofType(fromReports.GET_FIELDS)
    .map((action: fromReports.GetFields) => action.payload)
    .mergeMap((relatedField) => {
      const fieldReq: IGetRelatedFieldRequest = {
        model: relatedField.model_id,
        path: relatedField.path,
        field: relatedField.field_name,
      };
      return Observable.forkJoin(this.api.getRelatedFields(fieldReq),this.api.getFields(fieldReq))
        .map(([relatedFields, fields]) => new fromReports.GetFieldsSuccess({fields, relatedFields, parent: relatedField}));
    });
}
