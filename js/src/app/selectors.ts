import { State } from './reducers';
import { createSelector } from '@ngrx/store';
import * as reportSelectors from './selectors/reports';
import * as configSelectors from './selectors/config';

const getConfigState = (state: State) => state.config;
export const getIsAsyncReport = createSelector(
  getConfigState,
  configSelectors.getIsAsyncReport
);
export const getFormatOptions = createSelector(
  getConfigState,
  configSelectors.getFormatOptions
);

const getReportsState = (state: State) => state.reports;
export const getReports = createSelector(
  getReportsState,
  reportSelectors.getReports
);
export const getSelectedReport = createSelector(
  getReportsState,
  reportSelectors.getSelectedReport
);
export const getSelectedReportId = createSelector(
  getReportsState,
  reportSelectors.getSelectedReportId
);
export const getSelectedReportName = createSelector(
  getReportsState,
  reportSelectors.getSelectedReportName
);
export const getFields = createSelector(
  getReportsState,
  reportSelectors.getFields
);
export const getTitle = createSelector(
  getReportsState,
  reportSelectors.getTitle
);
export const getRightNavIsOpen = createSelector(
  getReportsState,
  reportSelectors.getRightNavIsOpen
);
export const getRelatedFields = createSelector(
  getReportsState,
  reportSelectors.getRelatedFields
);
export const getDescriptionInput = createSelector(
  getReportsState,
  reportSelectors.getDescriptionInput
);
export const getIsDistinct = createSelector(
  getReportsState,
  reportSelectors.getIsDistinct
);
export const getEditedReport = createSelector(
  getReportsState,
  reportSelectors.getEditedReport
);
export const getPreview = createSelector(
  getReportsState,
  reportSelectors.getPreview
);
export const getLastSaved = createSelector(
  getReportsState,
  reportSelectors.getLastSaved
);
export const getNewReportInfo = createSelector(
  getReportsState,
  reportSelectors.getNewReportInfo
);
export const getLastGeneratedReport = createSelector(
  getReportsState,
  reportSelectors.getLastGeneratedReport
);
export const getActiveTab = createSelector(
  getReportsState,
  reportSelectors.getActiveTab
);
export const getDisplayFields = createSelector(
  getReportsState,
  reportSelectors.getDisplayFields
);
export const getFilters = createSelector(
  getReportsState,
  reportSelectors.getFilters
);
export const getSelectedField = createSelector(
  getReportsState,
  reportSelectors.getSelectedField
);
export const isGeneratingReport = createSelector(
  getReportsState,
  reportSelectors.isGeneratingReport
);
export const hasEditedSinceLastSave = createSelector(
  getReportsState,
  reportSelectors.hasEditedSinceLastSave
);
export const getErrors = createSelector(
  getReportsState,
  reportSelectors.getErrors
);
