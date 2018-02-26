import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/do';
import 'rxjs/add/observable/forkJoin';

import { Injectable } from '@angular/core';

import { Effect, Actions } from '@ngrx/effects';
import { RouterNavigationAction, ROUTER_NAVIGATION } from '@ngrx/router-store';
import * as fromReports from '../actions/reports';
import * as fromRouter from '../actions/router';
import { RouterStateUrl, State } from '../reducers';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { Store } from '@ngrx/store';
import { hasEditedSinceLastSave } from '../selectors';
import { MatDialog } from '@angular/material';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../confirm/confirm-modal.component';

@Injectable()
export class RouterEffects {
  constructor(
    private actions$: Actions,
    private store$: Store<State>,
    private router: Router,
    private location: Location,
    public dialog: MatDialog
  ) {}

  @Effect({ dispatch: false })
  navigate$ = this.actions$
    .ofType(fromRouter.GO)
    .map((action: fromRouter.Go) => action.payload)
    .withLatestFrom(this.store$)
    .do(([{ path, query: queryParams, extras }, state]) => {
      const doNav = () =>
        this.router.navigate(path, { queryParams, ...extras });

      if (hasEditedSinceLastSave(state)) {
        const dialogRef = this.dialog.open(ConfirmModalComponent, {
          data: {
            title: 'Are you sure you want to navigate away from this report?',
            subtitle: 'All of your changes will be lost.',
          } as IConfirmModalData,
        });
        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            doNav();
          }
        });
        return;
      }
      doNav();
    });

  @Effect({ dispatch: false })
  navigateBack$ = this.actions$
    .ofType(fromRouter.BACK)
    .do(() => this.location.back());

  @Effect({ dispatch: false })
  navigateForward$ = this.actions$
    .ofType(fromRouter.FORWARD)
    .do(() => this.location.forward());

  @Effect()
  routeChange$ = this.actions$
    .ofType(ROUTER_NAVIGATION)
    .map((action: RouterNavigationAction<RouterStateUrl>) => {
      const route = action.payload.routerState;
      console.log(action.payload);
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
