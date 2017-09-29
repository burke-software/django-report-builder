import { createSelector } from '@ngrx/store';
import { IReport, IReportDetailed } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed;
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

    case reportActions.GET_REPORT: {
      return {
        ...state,
        selectedReport: null,
      };
    }

    case reportActions.GET_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
      };
    }

    default: {
      return state;
    }
  }
}

export const getReports = (state: State) => state.reports;
export const getSelectedReport = (state: State) => state.selectedReport;
