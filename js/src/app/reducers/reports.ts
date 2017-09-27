import { createSelector } from '@ngrx/store';
import { IReport } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
}

export const initialState: State = {
  reports: [],
};

export function reducer(state = initialState, action: reportActions.Actions): State {
  switch (action.type) {
    default: {
      return state;
    }
  }
}

export const getReports = (state: State) => state.reports;
