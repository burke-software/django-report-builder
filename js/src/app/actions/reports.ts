import { Action } from '@ngrx/store';
import {
  IReport,
  IReportDetailed,
  IRelatedField,
  IField,
  IReportPreview,
  INewReport,
  IBase,
} from '../api.interfaces';

export const GET_REPORT_LIST = 'Get Report List';
export const SET_REPORT_LIST = 'Set Report List';
export const GET_REPORT = 'Get Report';
export const GET_TITLE = 'Get Title';
export const GET_REPORT_SUCCESS = 'Get Report Success';
export const GET_REPORT_FIELDS_SUCCESS = 'Get Report Fields Success';
export const GET_FIELDS = 'Get Fields';
export const GET_FIELDS_SUCCESS = 'Get Fields Success';
export const GET_RELATED_FIELDS = 'Get Related Fields';
export const GET_RELATED_FIELDS_SUCCESS = 'Get Related Fields Success';
export const CHANGE_REPORT_DESCRIPTION = 'Change Report Description';
export const TOGGLE_REPORT_DISTINCT = 'Toggle Report Distinct';
export const DELETE_REPORT = 'Delete Report';
export const DELETE_REPORT_SUCCESS = 'Delete Report Success';
export const EDIT_REPORT = 'Edit Report';
export const EDIT_REPORT_SUCCESS = 'Edit Report Success';
export const GENERATE_PREVIEW = 'Generate Preview';
export const GENERATE_PREVIEW_SUCCESS = 'Generate Preview Success';
export const EXPORT_REPORT = 'Export Report';
export const CREATE_REPORT = 'Create Report';
export const CREATE_REPORT_SUCCESS = 'Create Report Success';
export const DOWNLOAD_EXPORTED_REPORT = 'Download Exported Report';
export const CHECK_EXPORT_STATUS = 'Check Export Status';
export const SET_FIELD_SEARCH_TEXT = 'Set Field Search Text';
export const SET_REPORT_SEARCH_TEXT = 'Set Report Search Text';
export const SET_RELATIONS_SEARCH_TEXT = 'Set Relations Search Text';
export const TOGGLE_LEFT_NAV = 'Toggle Left Nav';
export const SORT_REPORTS = 'Sort Reports';
export const TOGGLE_RIGHT_NAV = 'Toggle Right Nav';
export const CHANGE_TAB = 'Change Tab';
export const ADD_REPORT_FIELD = 'Add Report Field';
export const SELECT_FIELD = 'Select Field';

/** Request an updated list of all reports from the api */
export class GetReportList implements Action {
  readonly type = GET_REPORT_LIST;
}

export class SetReportList implements Action {
  readonly type = SET_REPORT_LIST;
  constructor(public payload: IReport[]) {}
}

/** Get the report details for one report for active editing */
export class GetReport implements Action {
  readonly type = GET_REPORT;
  constructor(public payload: number) {}
}

export class GetTitle implements Action {
  readonly type = GET_TITLE;
  constructor(public payload: string) {}
}

export class GetReportSuccess implements Action {
  readonly type = GET_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class GetReportFieldsSuccess implements Action {
  readonly type = GET_REPORT_FIELDS_SUCCESS;
  constructor(
    public payload: { relatedFields: IRelatedField[]; fields: IField[] }
  ) {}
}

export class GetFields implements Action {
  readonly type = GET_FIELDS;
  constructor(public payload: IRelatedField) {}
}

export class GetFieldsSuccess implements Action {
  readonly type = GET_FIELDS_SUCCESS;
  constructor(public payload: IField[]) {}
}

export class GetRelatedFields implements Action {
  readonly type = GET_RELATED_FIELDS;
  constructor(public payload: IRelatedField) {}
}

export class GetRelatedFieldsSuccess implements Action {
  readonly type = GET_RELATED_FIELDS_SUCCESS;
  constructor(
    public payload: { parent: IRelatedField; relatedFields: IRelatedField[] }
  ) {}
}

export class ChangeReportDescription implements Action {
  readonly type = CHANGE_REPORT_DESCRIPTION;
  constructor(public payload: string) {}
}

export class ToggleReportDistinct implements Action {
  readonly type = TOGGLE_REPORT_DISTINCT;
  constructor(public payload?: boolean) {}
}

export class DeleteReport implements Action {
  readonly type = DELETE_REPORT;
  constructor() {}
}

export class DeleteReportSuccess implements Action {
  readonly type = DELETE_REPORT_SUCCESS;
  constructor(public reportId: number) {}
}

export class EditReport implements Action {
  readonly type = EDIT_REPORT;
  constructor() {}
}

export class EditReportSuccess implements Action {
  readonly type = EDIT_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class GeneratePreview implements Action {
  readonly type = GENERATE_PREVIEW;
  constructor() {}
}

export class GeneratePreviewSuccess implements Action {
  readonly type = GENERATE_PREVIEW_SUCCESS;
  constructor(public payload: IReportPreview) {}
}

export class ExportReport implements Action {
  readonly type = EXPORT_REPORT;
  constructor(public payload: string) {}
}

export class DownloadExportedReport implements Action {
  readonly type = DOWNLOAD_EXPORTED_REPORT;
  constructor(public payload: string) {}
}

export class CheckExportStatus implements Action {
  readonly type = CHECK_EXPORT_STATUS;
  constructor(public payload: { reportId: string | number; taskId: string }) {}
}

export class CreateReport implements Action {
  readonly type = CREATE_REPORT;
  constructor(public payload: INewReport) {}
}

export class CreateReportSuccess implements Action {
  readonly type = CREATE_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class SetReportSearchText implements Action {
  readonly type = SET_REPORT_SEARCH_TEXT;
  constructor(public payload: string) {}
}

export class SetFieldSearchText implements Action {
  readonly type = SET_FIELD_SEARCH_TEXT;
  constructor(public payload: string) {}
}

export class SetRelationsSearchText implements Action {
  readonly type = SET_RELATIONS_SEARCH_TEXT;
  constructor(public payload: string) {}
}

export class ToggleLeftNav implements Action {
  readonly type = TOGGLE_LEFT_NAV;
}

export class ToggleRightNav implements Action {
  readonly type = TOGGLE_RIGHT_NAV;
}

export class SortReports implements Action {
  readonly type = SORT_REPORTS;
  constructor(public payload: string) {}
}

export class ChangeTab implements Action {
  readonly type = CHANGE_TAB;
  constructor(public payload: number) {}
}

export class AddReportField implements Action {
  readonly type = ADD_REPORT_FIELD;
  constructor(public payload: IBase) {}
}

export class SelectField implements Action {
  readonly type = SELECT_FIELD;
  constructor(public payload: IField) {}
}

export type Actions =
  | GetReportList
  | GetReportFieldsSuccess
  | SetReportList
  | GetReport
  | GetTitle
  | GetReportSuccess
  | GetFields
  | GetFieldsSuccess
  | GetRelatedFields
  | GetRelatedFieldsSuccess
  | ChangeReportDescription
  | ToggleReportDistinct
  | DeleteReport
  | DeleteReportSuccess
  | EditReport
  | EditReportSuccess
  | GeneratePreview
  | GeneratePreviewSuccess
  | ExportReport
  | CreateReport
  | CreateReportSuccess
  | DownloadExportedReport
  | CheckExportStatus
  | SetReportSearchText
  | SetFieldSearchText
  | SetRelationsSearchText
  | ToggleLeftNav
  | SortReports
  | ToggleRightNav
  | SortReports
  | ChangeTab
  | AddReportField
  | SelectField;
