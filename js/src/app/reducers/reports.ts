import { createSelector } from '@ngrx/store';
import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';
import {
  IReport,
  IReportDetailed,
  INestedRelatedField,
  IField,
  IDisplayField,
  IRelatedField,
  IReportPreview
} from '../api.interfaces';
import * as reportActions from '../actions/reports';
import {
  DisplayFieldActions,
  DisplayFieldActionTypes
} from '../actions/display-field';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: INestedRelatedField[];
  fields: IField[];
  title: string;
  descriptionInput: string;
  isDistinct: boolean;
  reportPreview?: IReportPreview;
  reportSaved?: Date;
  reportSearchText: string;
  fieldSearchText: string;
  relationsSearchText: string;
  leftNavIsOpen: boolean;
  rightNavIsOpen: boolean;
  activeTab: number;
  displayFields: EntityState<IDisplayField>;
}

export const displayFieldAdapter: EntityAdapter<
  IDisplayField
> = createEntityAdapter<IDisplayField>();

export const initialState: State = {
  reports: [],
  selectedReport: null,
  relatedFields: [],
  fields: [],
  title: '',
  descriptionInput: '',
  isDistinct: false,
  reportSearchText: '',
  fieldSearchText: '',
  relationsSearchText: '',
  leftNavIsOpen: false,
  rightNavIsOpen: false,
  activeTab: 0,
  displayFields: displayFieldAdapter.getInitialState()
};

export function reducer(
  state = initialState,
  action: reportActions.Actions | DisplayFieldActions
): State {
  switch (action.type) {
    case reportActions.SET_REPORT_LIST: {
      return {
        ...state,
        reports: action.payload
      };
    }

    case reportActions.GET_REPORT: {
      return {
        ...state,
        selectedReport: null,
        descriptionInput: initialState.descriptionInput
      };
    }

    case reportActions.GET_TITLE: {
      return {
        ...state,
        title: action.payload
      };
    }


    case reportActions.TOGGLE_LEFT_NAV: {
      return {
        ...state,
        leftNavIsOpen: !state.leftNavIsOpen
      };
    }

    case reportActions.TOGGLE_RIGHT_NAV: {
      return {
        ...state,
        rightNavIsOpen: !state.rightNavIsOpen
      };
    }

    case reportActions.GET_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        relatedFields: initialState.relatedFields,
        fields: initialState.fields,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct
      };
    }

    case reportActions.GET_REPORT_FIELDS_SUCCESS: {
      const relatedFields: INestedRelatedField[] = action.payload.relatedFields.map(
        relatedField => {
          return { ...relatedField, children: [] };
        }
      );
      return {
        ...state,
        relatedFields: relatedFields,
        fields: action.payload.fields
      };
    }

    case reportActions.GET_FIELDS_SUCCESS: {
      return {
        ...state,
        fields: action.payload
      };
    }

    case reportActions.GET_RELATED_FIELDS_SUCCESS: {
      return {
        ...state,
        relatedFields: state.relatedFields.map(
          populateChildren(action.payload.parent, action.payload.relatedFields)
        )
      };
    }

    case reportActions.CHANGE_REPORT_DESCRIPTION: {
      return {
        ...state,
        descriptionInput: action.payload
      };
    }

    case reportActions.TOGGLE_REPORT_DISTINCT: {
      return {
        ...state,
        isDistinct:
          action.payload !== undefined ? action.payload : !state.isDistinct
      };
    }

    case reportActions.EDIT_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct,
        reportSaved: new Date()
      };
    }

    case reportActions.GENERATE_PREVIEW_SUCCESS: {
      return {
        ...state,
        reportPreview: action.payload
      };
    }

    case reportActions.DELETE_REPORT_SUCCESS: {
      return {
        ...state,
        reports: state.reports.filter(r => r.id !== action.reportId),
        selectedReport: initialState.selectedReport
      };
    }

    case reportActions.DOWNLOAD_EXPORTED_REPORT: {
      return {
        ...state,
        selectedReport: Object.assign({}, state.selectedReport, {
          report_file: action.payload,
          report_file_creation: new Date().toISOString()
        })
      };
    }

    case reportActions.SET_REPORT_SEARCH_TEXT: {
      console.log(action.payload);
      return {
        ...state,
        reportSearchText: action.payload
      };
    }

    case reportActions.SET_FIELD_SEARCH_TEXT: {
      console.log(action.payload);
      return {
        ...state,
        fieldSearchText: action.payload
      };
    }

    case reportActions.SET_RELATIONS_SEARCH_TEXT: {
      return {
        ...state,
        relationsSearchText: action.payload
      };
    }

    case reportActions.CHANGE_TAB: {
      return {
        ...state,
        activeTab: action.payload
      };
    }

    case DisplayFieldActionTypes.ADD_ONE:
      return {
        ...state,
        displayFields: displayFieldAdapter.addOne(
          action.payload,
          state.displayFields
        )
      };

    default: {
      return state;
    }
  }
}

function populateChildren(parent: IRelatedField, children: IRelatedField[]) {
  return function replaceField(
    field: INestedRelatedField
  ): INestedRelatedField {
    const replacement = { ...field };
    if (field === parent) {
      replacement.children = [...children].map(child => ({
        ...child,
        children: []
      }));
    } else {
      replacement.children = replacement.children.map(replaceField);
    }
    return replacement;
  };
}

export const getReports = (state: State) => state.reports;
export const getTitle = (state: State) => state.title;
export const getSelectedReport = (state: State) => state.selectedReport;
export const getSelectedReportId = (state: State) => {
  const report = getSelectedReport(state);
  if (report) {
    return report.id;
  }
};
export const getFields = (state: State) => state.fields;
export const getRelatedFields = (state: State) => state.relatedFields;
export const getDescriptionInput = (state: State) => state.descriptionInput;
export const getIsDistinct = (state: State) => state.isDistinct;
export const getEditedReport = (state: State) => {
  const editedReport = { ...state.selectedReport };
  editedReport.description = state.descriptionInput;
  editedReport.distinct = state.isDistinct;
  return editedReport;
};
export const getPreview = (state: State) => state.reportPreview;
export const getLastSaved = (state: State) => state.reportSaved;
export const getNewReportInfo = (state: State) => {
  const report = getSelectedReport(state);
  if (report) {
    const { name, description, root_model } = report;
    return { name, description, root_model };
  }
};
export const getLastGeneratedReport = createSelector(
  getSelectedReport,
  selectedReport => {
    if (selectedReport) {
      const { report_file, report_file_creation } = selectedReport;
      return { report_file, report_file_creation };
    }
  }
);
export const getReportSearchTerm = (state: State) => state.reportSearchText;
export const getFieldSearchTerm = (state: State) => state.fieldSearchText;
export const getRelationsSearchTerm = (state: State) =>
  state.relationsSearchText;
export const getLeftNavIsOpen = (state: State) => state.leftNavIsOpen;
export const getRightNavIsOpen = (state: State) => state.rightNavIsOpen;

export const getDisplayFieldsState = (state: State) => state.displayFields;
const {
  selectIds: notSelectIds,
  selectEntities: notSelectEntities,
  selectAll: notSelectAll,
  selectTotal: notSelectTotal
} = displayFieldAdapter.getSelectors();
export const selectIds = createSelector(getDisplayFieldsState, notSelectIds);
export const selectEntities = createSelector(
  getDisplayFieldsState,
  notSelectEntities
);
export const selectAll = createSelector(getDisplayFieldsState, notSelectAll);
export const selectTotal = createSelector(
  getDisplayFieldsState,
  notSelectTotal
);
