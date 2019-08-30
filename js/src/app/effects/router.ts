import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { Effect, Actions, ofType } from '@ngrx/effects';
import { RouterNavigationAction, ROUTER_NAVIGATION } from '@ngrx/router-store';
import { tap, map, filter } from 'rxjs/operators';

import * as fromReports from '../actions/reports';
import { RouterActionTypes, Go } from '../actions/router';
import { RouterStateUrl } from '../reducers';

@Injectable()
export class RouterEffects {
  constructor(
    private actions$: Actions,
    private router: Router,
    private location: Location
  ) {}

  @Effect({ dispatch: false })
  navigate$ = this.actions$.pipe(
    ofType(RouterActionTypes.GO),
    map((action: Go) => action.payload),
    tap(({ path, query: queryParams, extras }) =>
      this.router.navigate(path, { queryParams, ...extras })
    )
  );

  @Effect({ dispatch: false })
  navigateBack$ = this.actions$.pipe(
    ofType(RouterActionTypes.BACK),
    tap(() => this.location.back())
  );

  @Effect({ dispatch: false })
  navigateForward$ = this.actions$.pipe(
    ofType(RouterActionTypes.FORWARD),
    tap(() => this.location.forward())
  );

  @Effect()
  routeChange$ = this.actions$.pipe(
    ofType(ROUTER_NAVIGATION),
    map((action: RouterNavigationAction<RouterStateUrl>) => {
      const route = action.payload.routerState;
      if (route.url === '/') {
        return new fromReports.GetReportList();
      }
      if (route.params.id) {
        return new fromReports.GetReport(route.params.id);
      }
      return null;
    }),
    filter(Boolean)
  );
}
