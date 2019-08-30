import { Observable } from 'rxjs';

import { Injectable } from '@angular/core';
import { Effect, Actions, ofType } from '@ngrx/effects';
import { Action } from '@ngrx/store';
import { ConfigActionTypes, GetConfigSuccess } from '../actions/config';
import { ApiService } from '../api.service';
import { mergeMap, map } from 'rxjs/operators';

@Injectable()
export class ConfigEffects {
  constructor(private actions$: Actions, private api: ApiService) {}

  @Effect()
  getConfig$: Observable<Action> = this.actions$.pipe(
    ofType(ConfigActionTypes.GET_CONFIG),
    mergeMap(() =>
      this.api.getConfig().pipe(map(response => new GetConfigSuccess(response)))
    )
  );
}
