import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/do';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/withLatestFrom';
import 'rxjs/add/observable/forkJoin';

import { Injectable } from '@angular/core';
import { Effect, Actions } from '@ngrx/effects';
import { Action } from '@ngrx/store';
import * as fromConfig from '../actions/config';
import { ApiService } from '../api.service';

@Injectable()
export class ConfigEffects {
  constructor(
    private actions$: Actions,
    private api: ApiService,
  ) {}

  @Effect()
  getConfig$: Observable<Action> = this.actions$
    .ofType(fromConfig.GET_CONFIG)
    .mergeMap(() => this.api.getConfig().map(response => new fromConfig.GetConfigSuccess(response)));
}
