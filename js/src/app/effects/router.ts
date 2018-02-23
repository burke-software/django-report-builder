import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/do';

import { Injectable } from '@angular/core';

import { Effect, Actions } from '@ngrx/effects';
import { RouterNavigationAction, ROUTER_NAVIGATION } from '@ngrx/router-store';
import * as fromReports from '../actions/reports';

@Injectable()
export class RouterEffects {
  constructor(private actions$: Actions) {}

  @Effect()
  routeChange$ = this.actions$
    .ofType(ROUTER_NAVIGATION)
    .map((action: RouterNavigationAction) => {
      const route = action.payload.routerState;
      if (route.url === '/') {
        return new fromReports.GetReportList();
      }
      if (route.root.params.id) {
        return new fromReports.GetReport(route.root.params.id);
      }
      return null;
    })
    .filter(Boolean);
}
