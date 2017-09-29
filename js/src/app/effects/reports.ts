import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/do';

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Effect, Actions } from '@ngrx/effects';
import { Observable } from 'rxjs/Observable';
import { Action } from '@ngrx/store';

import { ApiService } from '../api.service';
import * as fromReports from '../actions/reports';

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

  @Effect({dispatch: false})
  getReportSuccess$ = this.actions$
    .ofType(fromReports.GET_REPORT_SUCCESS)
    .map((action: fromReports.GetReportSuccess) => action.payload)
    .do((report) => this.router.navigate(['/report', report.id]));
}
