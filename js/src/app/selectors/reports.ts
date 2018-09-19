import { State, displayFieldAdapter, filterAdapter } from '../models/reports';
import { createSelector } from '@ngrx/store';

export const getReports = (state: State) => state.reports;
export const getTitle = (state: State) => state.title;
export const getSelectedReport = (state: State) => state.selectedReport;
export const getSelectedReportId = createSelector(
  getSelectedReport,
  report => report && report.id
);
export const getSelectedReportName = createSelector(
  getSelectedReport,
  report => report && report.name
);
export const getFields = (state: State) => state.fields;
export const getRelatedFields = (state: State) => state.relatedFields;
export const getDescriptionInput = (state: State) => state.descriptionInput;
export const getTitleInput = (state: State) => state.titleInput;
export const getIsDistinct = (state: State) => state.isDistinct;
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
    if (selectedReport && selectedReport.report_file) {
      const { report_file, report_file_creation } = selectedReport;
      return { report_file, report_file_creation };
    }
  }
);
export const getRightNavIsOpen = (state: State) => state.rightNavIsOpen;

export const getDisplayFieldsState = (state: State) => state.displayFields;
const {
  selectAll: selectAllDisplayFields,
  selectTotal: selectDisplayFieldsCount,
} = displayFieldAdapter.getSelectors();
export const getDisplayFields = createSelector(
  getDisplayFieldsState,
  selectAllDisplayFields
);
export const getDisplayFieldsCount = createSelector(
  getDisplayFieldsState,
  selectDisplayFieldsCount
);
export const getFiltersState = (state: State) => state.filters;
const {
  selectAll: selectAllFilters,
  selectTotal: selectFiltersCount,
} = filterAdapter.getSelectors();
export const getFilters = createSelector(getFiltersState, selectAllFilters);
export const getFiltersCount = createSelector(
  getFiltersState,
  selectFiltersCount
);
export const getActiveTab = (state: State) => state.activeTab;

export const getEditedReport = (state: State) => ({
  ...state.selectedReport,
  description: getDescriptionInput(state),
  distinct: getIsDistinct(state),
  displayfield_set: getDisplayFields(state),
  filterfield_set: getFilters(state),
  name: getTitleInput(state),
});
export const getSelectedField = (state: State) => state.selectedField;
export const isGeneratingReport = (state: State) => state.generatingReport;
export const hasEditedSinceLastSave = (state: State) =>
  state.editedSinceLastSave;
export const getErrors = (state: State) => state.errors;
