import { ActionReducerMap, MetaReducer } from '@ngrx/store';
import { Params, RouterStateSnapshot } from '@angular/router';
import {
  routerReducer,
  RouterReducerState,
  RouterStateSerializer,
} from '@ngrx/router-store';
import { environment } from '../environments/environment';

import { storeFreeze } from 'ngrx-store-freeze';

import { reducer as reportReducer } from './reducers/reports';
import { reducer as configReducer } from './reducers/config';

import { State as ReportsState } from './models/reports';
import { State as ConfigState } from './models/config';
import { Injectable } from "@angular/core";

export interface RouterStateUrl {
  url: string;
  params: Params;
  queryParams: Params;
}

export interface State {
  reports: ReportsState;
  config: ConfigState;
  router: RouterReducerState<RouterStateUrl>;
}

// https://github.com/ngrx/platform/blob/master/docs/router-store/api.md#custom-router-state-serializer
@Injectable()
export class CustomSerializer implements RouterStateSerializer<RouterStateUrl> {
  serialize(routerState: RouterStateSnapshot): RouterStateUrl {
    let route = routerState.root;

    while (route.firstChild) {
      route = route.firstChild;
    }

    const { url, root: { queryParams } } = routerState;
    const { params } = route;

    // Only return an object including the URL, params and query params
    // instead of the entire snapshot
    return { url, params, queryParams };
  }
}

export const reducers: ActionReducerMap<State> = {
  reports: reportReducer,
  config: configReducer,
  router: routerReducer,
};

export const metaReducers: MetaReducer<State>[] = !environment.production
  ? [storeFreeze]
  : [];
