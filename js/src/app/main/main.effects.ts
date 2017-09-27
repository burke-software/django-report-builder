import 'rxjs/add/operator/mergeMap';

import { Injectable } from '@angular/core';
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
  ) {}
}

