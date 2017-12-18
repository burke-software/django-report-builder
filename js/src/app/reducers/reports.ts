import { IReport, IReportDetailed, IRelatedField, IField } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: IRelatedField[];
  fields: IField[];
}

export const initialState: State = {
  reports: [],
  selectedReport: null,
  relatedFields: [],
  fields: [],
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
        relatedFields: initialState.relatedFields,
        fields: initialState.fields,
      };
    }

    case reportActions.GET_REPORT_FIELDS_SUCCESS: {
      return {
        ...state,
        relatedFields: action.payload.relatedFields,
        fields: action.payload.fields,
      };
    }

    default: {
      return state;
    }
  }
}

export const getReports = (state: State) => state.reports;
export const getSelectedReport = (state: State) => state.selectedReport;
