import {
    ActionReducerMap,
    createSelector,
    MetaReducer,
  } from '@ngrx/store';
import { environment } from '../environments/environment';

import { storeFreeze } from 'ngrx-store-freeze';

import * as fromReports from './reducers/reports';
import * as fromDisplayField from './reducers/display-field';

export interface State {
  reports: fromReports.State;
  displayFields: fromDisplayField.State;
}

export const reducers: ActionReducerMap<State> = {
  reports: fromReports.reducer,
  displayFields: fromDisplayField.reducer,
};

export const metaReducers: MetaReducer<State>[] = !environment.production
? [storeFreeze]
: [];

const getReportsState = (state: State) => state.reports;
export const getReports = createSelector(getReportsState, fromReports.getReports);
export const getSelectedReport = createSelector(getReportsState, fromReports.getSelectedReport);
export const getFields = createSelector(getReportsState, fromReports.getFields);
export const getRelatedFields = createSelector(getReportsState, fromReports.getRelatedFields);
export const getDescriptionInput = createSelector(getReportsState, fromReports.getDescriptionInput);
