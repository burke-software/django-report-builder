import { ActionReducerMap, MetaReducer } from '@ngrx/store';
import { environment } from '../environments/environment';

import { storeFreeze } from 'ngrx-store-freeze';

import { reducer as reportReducer } from './reducers/reports';
import { reducer as configReducer } from './reducers/config';

import { State as ReportsState } from './models/reports';
import { State as ConfigState } from './models/config';

export interface State {
  reports: ReportsState;
  config: ConfigState;
}

export const reducers: ActionReducerMap<State> = {
  reports: reportReducer,
  config: configReducer,
};

export const metaReducers: MetaReducer<State>[] = !environment.production
  ? [storeFreeze]
  : [];
