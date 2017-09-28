import { createSelector } from '@ngrx/store';
import { IReport } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
  selectedReport: number;
}

export const initialState: State = {
  reports: [],
  selectedReport: null,
};

export function reducer(state = initialState, action: reportActions.Actions): State {
  switch (action.type) {
    case reportActions.SET_REPORT_LIST: {
      return {
        ...state,
        reports: action.payload,
      };
    }
    default: {
      return state;
    }
  }
}

export const getReports = (state: State) => state.reports;
