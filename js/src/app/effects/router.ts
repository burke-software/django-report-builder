import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/do';
import 'rxjs/add/observable/forkJoin';

import { Injectable } from '@angular/core';

import { Effect, Actions } from '@ngrx/effects';
import { RouterNavigationAction, ROUTER_NAVIGATION } from '@ngrx/router-store';
import * as fromReports from '../actions/reports';
import { RouterActionTypes, Go } from '../actions/router';
import { RouterStateUrl } from '../reducers';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Injectable()
export class RouterEffects {
  constructor(
    private actions$: Actions,
    private router: Router,
    private location: Location
  ) {}

  @Effect({ dispatch: false })
  navigate$ = this.actions$
    .ofType(RouterActionTypes.GO)
    .map((action: Go) => action.payload)
    .do(({ path, query: queryParams, extras }) =>
      this.router.navigate(path, { queryParams, ...extras })
    );

  @Effect({ dispatch: false })
  navigateBack$ = this.actions$
    .ofType(RouterActionTypes.BACK)
    .do(() => this.location.back());

  @Effect({ dispatch: false })
  navigateForward$ = this.actions$
    .ofType(RouterActionTypes.FORWARD)
    .do(() => this.location.forward());

  @Effect()
  routeChange$ = this.actions$
    .ofType(ROUTER_NAVIGATION)
    .map((action: RouterNavigationAction<RouterStateUrl>) => {
      const route = action.payload.routerState;
      if (route.url === '/') {
        return new fromReports.GetReportList();
      }
      if (route.params.id) {
        return new fromReports.GetReport(route.params.id);
      }
      return null;
    })
    .filter(Boolean);
}
