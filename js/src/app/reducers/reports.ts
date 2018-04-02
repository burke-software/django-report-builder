import { State, displayFieldAdapter, filterAdapter } from '../models/reports';
import { INestedRelatedField, IReportErrors } from '../models/api';
import { ReportActionTypes, ReportActions } from '../actions/reports';
import {
  DisplayFieldActions,
  DisplayFieldActionTypes,
} from '../actions/display-field';
import { FilterActions, FilterActionTypes } from '../actions/filter';
import * as selectors from '../selectors/reports';

export const initialState: State = {
  reports: [],
  selectedReport: null,
  relatedFields: [],
  fields: [],
  title: '',
  titleInput: '',
  descriptionInput: '',
  isDistinct: false,
  rightNavIsOpen: false,
  activeTab: 0,
  displayFields: displayFieldAdapter.getInitialState(),
  filters: filterAdapter.getInitialState(),
  nextRelatedFieldId: 0,
  generatingReport: false,
  editedSinceLastSave: false,
};

export function reducer(
  state = initialState,
  action: ReportActions | DisplayFieldActions | FilterActions
): State {
  switch (action.type) {
    case ReportActionTypes.SET_REPORT_LIST: {
      return {
        ...state,
        reports: action.payload,
      };
    }

    case ReportActionTypes.GET_REPORT: {
      // Reset report state when we start making a new request
      // so the user never sees stale data
      const {selectedReport, activeTab, descriptionInput, reportPreview} = initialState
      return {
        ...state,
        selectedReport,
        activeTab,
        descriptionInput,
        reportPreview
      };
    }

    case ReportActionTypes.GET_TITLE: {
      return {
        ...state,
        title: action.payload,
      };
    }

    case ReportActionTypes.TOGGLE_RIGHT_NAV: {
      let navOpen = !state.rightNavIsOpen;
      if (state.activeTab === 2 || state.activeTab === 3) {
        navOpen = false;
      } else if (action.payload !== undefined) {
        navOpen = action.payload;
      }
      return {
        ...state,
        rightNavIsOpen: navOpen,
      };
    }

    case ReportActionTypes.GET_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        relatedFields: selectors.getRelatedFields(initialState),
        fields: selectors.getFields(initialState),
        descriptionInput: action.payload.description,
        titleInput: action.payload.name,
        isDistinct: action.payload.distinct,
        editedSinceLastSave: false,
      };
    }

    case ReportActionTypes.GET_REPORT_FIELDS_SUCCESS: {
      let { nextRelatedFieldId } = state;
      const selectedReport = selectors.getSelectedReport(state);

      const rootRelatedField: INestedRelatedField = {
        id: nextRelatedFieldId++,
        children: action.payload.relatedFields.map(relatedField => {
          const id = nextRelatedFieldId++;
          return { ...relatedField, children: [], id };
        }),
        field_name: '',
        verbose_name: selectedReport.root_model_name,
        path: '',
        help_text:
          'The root model for this report: ' + selectedReport.root_model_name,
        model_id: selectedReport.root_model,
        parent_model_name: '',
        parent_model_app_label: false,
        included_model: true,
      };
      return {
        ...state,
        relatedFields: [rootRelatedField],
        fields: action.payload.fields,
        nextRelatedFieldId,
      };
    }

    case ReportActionTypes.GET_FIELDS_SUCCESS: {
      return {
        ...state,
        fields: action.payload,
      };
    }

    case ReportActionTypes.GET_RELATED_FIELDS_SUCCESS: {
      let { nextRelatedFieldId } = state;
      const relatedFields: INestedRelatedField[] = action.payload.relatedFields.map(
        relatedField => {
          const id = nextRelatedFieldId++;
          return { ...relatedField, children: [], id };
        }
      );
      return {
        ...state,
        nextRelatedFieldId,
        relatedFields: selectors
          .getRelatedFields(state)
          .map(populateChildren(action.payload.parentId, relatedFields)),
      };
    }

    case ReportActionTypes.CHANGE_REPORT_DESCRIPTION: {
      return {
        ...state,
        descriptionInput: action.payload,
        editedSinceLastSave: true,
      };
    }

    case ReportActionTypes.CHANGE_REPORT_TITLE: {
      return {
        ...state,
        titleInput: action.payload,
        editedSinceLastSave: true,
      };
    }

    case ReportActionTypes.TOGGLE_REPORT_DISTINCT: {
      return {
        ...state,
        isDistinct:
          action.payload !== undefined ? action.payload : !state.isDistinct,
      };
    }

    case ReportActionTypes.EDIT_REPORT_SUCCESS: {
      return {
        ...state,
        selectedReport: action.payload,
        descriptionInput: action.payload.description,
        isDistinct: action.payload.distinct,
        reportSaved: new Date(),
        editedSinceLastSave: false,
        errors: undefined,
      };
    }

    case ReportActionTypes.EDIT_REPORT_FAILURE: {
      return {
        ...state,
        errors: flatten(
          Object.entries(action.payload).map(([tab, items]) => {
            if (typeof items[0] === 'string') {
              return (items as string[]).map(
                e => `Your ${tab} field has the error: ${e}`
              );
            } else {
              return (items as IReportErrors[]).map((item, i) =>
                Object.entries(item).map(([itemName, errors]) =>
                  (errors as string[]).map(
                    e =>
                      `In ${tab}, your ${i} field's ${itemName} has the error: ${e}`
                  )
                )
              );
            }
          })
        ),
      };
    }

    case ReportActionTypes.EXPORT_REPORT: {
      return {
        ...state,
        generatingReport: true,
      };
    }

    case ReportActionTypes.CANCEL_EXPORT_REPORT: {
      return {
        ...state,
        generatingReport: false,
      };
    }

    case ReportActionTypes.DOWNLOAD_EXPORTED_REPORT: {
      return {
        ...state,
        generatingReport: false,
        errors: undefined,
      };
    }

    case ReportActionTypes.GENERATE_PREVIEW: {
      return { ...state, generatingReport: true };
    }

    case ReportActionTypes.GENERATE_PREVIEW_SUCCESS: {
      return {
        ...state,
        reportPreview: action.payload,
        generatingReport: false,
        errors: undefined,
      };
    }

    case ReportActionTypes.CANCEL_GENERATE_PREVIEW: {
      return {
        ...state,
        reportPreview: undefined,
        generatingReport: false,
      };
    }

    case ReportActionTypes.DELETE_REPORT_SUCCESS: {
      return {
        ...state,
        reports: state.reports.filter(r => r.id !== action.reportId),
        selectedReport: selectors.getSelectedReport(initialState),
        editedSinceLastSave: false,
      };
    }

    case ReportActionTypes.DOWNLOAD_EXPORTED_REPORT: {
      return {
        ...state,
        selectedReport: {
          ...selectors.getSelectedReport(state),
          report_file: action.payload,
          report_file_creation: new Date().toISOString(),
        },
      };
    }

    case ReportActionTypes.CHANGE_TAB: {
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
        editedSinceLastSave: true,
      };

    case DisplayFieldActionTypes.UPDATE_MANY:
      return {
        ...state,
        displayFields: displayFieldAdapter.updateMany(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
        editedSinceLastSave: true,
      };

    case DisplayFieldActionTypes.DELETE_ONE:
      return {
        ...state,
        displayFields: displayFieldAdapter.removeOne(
          action.payload,
          selectors.getDisplayFieldsState(state)
        ),
        editedSinceLastSave: true,
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
        editedSinceLastSave: true,
      };

    case FilterActionTypes.UPDATE_MANY:
      return {
        ...state,
        filters: filterAdapter.updateMany(
          action.payload,
          selectors.getFiltersState(state)
        ),
        editedSinceLastSave: true,
      };

    case FilterActionTypes.DELETE_ONE:
      return {
        ...state,
        filters: filterAdapter.removeOne(
          action.payload,
          selectors.getFiltersState(state)
        ),
        editedSinceLastSave: true,
      };

    case ReportActionTypes.ADD_REPORT_FIELD: {
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
            editedSinceLastSave: true,
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
                filter_value: ''
              },
              selectors.getFiltersState(state)
            ),
            editedSinceLastSave: true,
          };

        default:
          return state;
      }
    }

    case ReportActionTypes.SELECT_FIELD: {
      return {
        ...state,
        selectedField: action.payload,
      };
    }

    default:
      return state;
  }
}

function populateChildren(parentId: number, children: INestedRelatedField[]) {
  return function replaceField(
    field: INestedRelatedField
  ): INestedRelatedField {
    const replacement = { ...field };
    if (field.id === parentId) {
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

function flatten(items) {
  const flat = [];

  items.forEach(item => {
    if (Array.isArray(item)) {
      flat.push(...flatten(item));
    } else {
      flat.push(item);
    }
  });

  return flat;
}
