import { IReport, IReportDetailed, INestedRelatedField, IField, IRelatedField } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: INestedRelatedField[];
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
      const relatedFields: INestedRelatedField[] = action.payload.relatedFields.map((relatedField) => {
        return {...relatedField, children: []};
      });
      return {
        ...state,
        relatedFields: relatedFields,
        fields: action.payload.fields,
      };
    }

    case reportActions.GET_FIELDS_SUCCESS: {
      return {
        ...state,
        fields: action.payload,
      };
    }

    case reportActions.GET_RELATED_FIELDS_SUCCESS: {
      return {
        ...state,
        relatedFields: state.relatedFields.map(populateChildren(action.payload.parent, action.payload.relatedFields))
      };
    }

    default: {
      return state;
    }
  }
}

function populateChildren(parent: IRelatedField, children: IRelatedField[]) {
  return function replaceField(field: INestedRelatedField): INestedRelatedField {
    const replacement = {...field};
    if (field === parent) {
      replacement.children = [...children].map(child => ({...child, children: []}));
    } else {
      replacement.children = replacement.children.map(replaceField);
    }
    return replacement;
  };
}

export const getReports = (state: State) => state.reports;
export const getSelectedReport = (state: State) => state.selectedReport;
export const getFields = (state: State) => state.fields;
export const getRelatedFields = (state: State) => state.relatedFields;
