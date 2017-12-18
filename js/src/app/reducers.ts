import {
    ActionReducerMap,
    createSelector,
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

const getReportsState = (state: State) => state.reports;
export const getReports = createSelector(getReportsState, fromReports.getReports);
export const getSelectedReport = createSelector(getReportsState, fromReports.getSelectedReport);
