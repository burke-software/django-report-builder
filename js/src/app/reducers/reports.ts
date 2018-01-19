import { IReport, IReportDetailed, INestedRelatedField, IField, IRelatedField } from '../api.interfaces';
import * as reportActions from '../actions/reports';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: INestedRelatedField[];
  fields: IField[];
  descriptionInput: string;
  isDistinct: boolean;
}

export const initialState: State = {
  reports: [],
  selectedReport: null,
  relatedFields: [],
  fields: [],
  descriptionInput: '',
  isDistinct: false,
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
        descriptionInput: initialState.descriptionInput,
      };
    }

    case reportActions.GET_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        relatedFields: initialState.relatedFields,
        fields: initialState.fields,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct,
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

    case reportActions.CHANGE_REPORT_DESCRIPTION: {
      return {
        ...state,
        descriptionInput: action.payload,
      };
    }

    case reportActions.TOGGLE_REPORT_DISTINCT: {
      return {
        ...state,
        isDistinct: action.payload !== undefined ? action.payload : !state.isDistinct
      };
    }

    case reportActions.EDIT_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct
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
export const getSelectedReportId = (state: State) => getSelectedReport(state).id;
export const getFields = (state: State) => state.fields;
export const getRelatedFields = (state: State) => state.relatedFields;
export const getDescriptionInput = (state: State) => state.descriptionInput;
export const getIsDistinct = (state: State) => state.isDistinct;
export const getEditedReport = (state: State) => {
  const editedReport = {...state.selectedReport};
  editedReport.description = state.descriptionInput;
  editedReport.distinct = state.isDistinct;
  return editedReport;
};
