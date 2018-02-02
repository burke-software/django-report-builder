import { INestedRelatedField, IRelatedField } from '../api.interfaces';
import * as reportActions from '../actions/reports';
import {
  DisplayFieldActions,
  DisplayFieldActionTypes,
} from '../actions/display-field';
import { FilterActions, FilterActionTypes } from '../actions/filter';
import * as selectors from './reports.selectors';
import { State, displayFieldAdapter, filterAdapter } from './reports.init';

export * from './reports.selectors';
export * from './reports.init';

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
  displayFields: displayFieldAdapter.getInitialState(),
  filters: filterAdapter.getInitialState(),
};

export function reducer(
  state = initialState,
  action: reportActions.Actions | DisplayFieldActions | FilterActions
): State {
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
        descriptionInput: selectors.getDescriptionInput(initialState),
      };
    }

    case reportActions.GET_TITLE: {
      return {
        ...state,
        title: action.payload,
      };
    }

    case reportActions.TOGGLE_LEFT_NAV: {
      return {
        ...state,
        leftNavIsOpen: !state.leftNavIsOpen,
      };
    }

    case reportActions.TOGGLE_RIGHT_NAV: {
      return {
        ...state,
        rightNavIsOpen: !state.rightNavIsOpen,
      };
    }

    case reportActions.GET_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        relatedFields: selectors.getRelatedFields(initialState),
        fields: selectors.getFields(initialState),
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct,
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
        relatedFields: selectors
          .getRelatedFields(state)
          .map(
            populateChildren(
              action.payload.parent,
              action.payload.relatedFields
            )
          ),
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
        isDistinct:
          action.payload !== undefined ? action.payload : !state.isDistinct,
      };
    }

    case reportActions.EDIT_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct,
        reportSaved: new Date(),
      };
    }

    case reportActions.GENERATE_PREVIEW_SUCCESS: {
      return {
        ...state,
        reportPreview: action.payload,
      };
    }

    case reportActions.DELETE_REPORT_SUCCESS: {
      return {
        ...state,
        reports: state.reports.filter(r => r.id !== action.reportId),
        selectedReport: selectors.getSelectedReport(initialState),
      };
    }

    case reportActions.DOWNLOAD_EXPORTED_REPORT: {
      return {
        ...state,
        selectedReport: {
          ...selectors.getSelectedReport(state),
          report_file: action.payload,
          report_file_creation: new Date().toISOString(),
        },
      };
    }

    case reportActions.SET_REPORT_SEARCH_TEXT: {
      return {
        ...state,
        reportSearchText: action.payload,
      };
    }

    case reportActions.SET_FIELD_SEARCH_TEXT: {
      return {
        ...state,
        fieldSearchText: action.payload,
      };
    }

    case reportActions.SET_RELATIONS_SEARCH_TEXT: {
      return {
        ...state,
        relationsSearchText: action.payload,
      };
    }

    case reportActions.CHANGE_TAB: {
      return {
        ...state,
        activeTab: action.payload,
      };
    }

    case DisplayFieldActionTypes.LOAD_ALL:
      return {
        ...state,
        displayFields: displayFieldAdapter.addAll(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
      };

    case DisplayFieldActionTypes.UPDATE_ONE:
      return {
        ...state,
        displayFields: displayFieldAdapter.updateOne(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
      };

    case DisplayFieldActionTypes.UPDATE_MANY:
      return {
        ...state,
        displayFields: displayFieldAdapter.updateMany(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
      };

    case DisplayFieldActionTypes.DELETE_ONE:
      return {
        ...state,
        displayFields: displayFieldAdapter.removeOne(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
      };

    case FilterActionTypes.LOAD_ALL:
      return {
        ...state,
        filters: filterAdapter.addAll(
          action.payload,
          selectors.getFiltersState(state)
        ),
      };

    case FilterActionTypes.UPDATE_ONE:
      return {
        ...state,
        filters: filterAdapter.updateOne(
          action.payload,
          selectors.getFiltersState(state)
        ),
      };

    case FilterActionTypes.UPDATE_MANY:
      return {
        ...state,
        filters: filterAdapter.updateMany(
          action.payload,
          selectors.getFiltersState(state)
        ),
      };

    case FilterActionTypes.DELETE_ONE:
      return {
        ...state,
        filters: filterAdapter.removeOne(
          action.payload,
          selectors.getFiltersState(state)
        ),
      };

    case reportActions.ADD_REPORT_FIELD: {
      switch (selectors.getActiveTab(state)) {
        case 0:
          return {
            ...state,
            displayFields: displayFieldAdapter.addOne(
              {
                ...action.payload,
                position: selectors.getDisplayFieldsCount(state),
                report: selectors.getSelectedReportId(state),
              },
              selectors.getDisplayFieldsState(state)
            ),
          };
        case 1:
          return {
            ...state,
            filters: filterAdapter.addOne(
              {
                ...action.payload,
                position: selectors.getFiltersCount(state),
                report: selectors.getSelectedReportId(state),
                filter_type: 'exact',
              },
              selectors.getFiltersState(state)
            ),
          };

        default:
          return state;
      }
    }

    case reportActions.SELECT_FIELD: {
      return {
        ...state,
        selectedField: action.payload,
      };
    }

    default:
      return state;
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
        children: [],
      }));
    } else {
      replacement.children = replacement.children.map(replaceField);
    }
    return replacement;
  };
}
