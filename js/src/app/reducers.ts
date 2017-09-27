import {
    ActionReducerMap,
    createSelector,
    createFeatureSelector,
    ActionReducer,
    MetaReducer,
  } from '@ngrx/store';
import { environment } from '../environments/environment';

import { storeFreeze } from 'ngrx-store-freeze';

import * as fromReports from './reducers/reports';

export interface State {
  reports: fromReports.State;
}

export const reducers: ActionReducerMap<State> = {
  reports: fromReports.reducer,
};

export const metaReducers: MetaReducer<State>[] = !environment.production
? [storeFreeze]
: [];

export const getReports = createSelector((state: State) => state.reports, fromReports.getReports);
