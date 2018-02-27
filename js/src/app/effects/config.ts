import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';

import { Injectable } from '@angular/core';
import { Effect, Actions } from '@ngrx/effects';
import { Action } from '@ngrx/store';
import { ConfigActionTypes, GetConfigSuccess } from '../actions/config';
import { ApiService } from '../api.service';

@Injectable()
export class ConfigEffects {
  constructor(private actions$: Actions, private api: ApiService) {}

  @Effect()
  getConfig$: Observable<Action> = this.actions$
    .ofType(ConfigActionTypes.GET_CONFIG)
    .mergeMap(() =>
      this.api.getConfig().map(response => new GetConfigSuccess(response))
    );
}
