import { Action } from '@ngrx/store';
import {
  IReport,
  IReportDetailed,
  IRelatedField,
  IField,
  IReportPreview,
  INewReport,
  IBase,
  INestedRelatedField,
  IExportType,
  IReportErrors,
} from '../models/api';

export enum ReportActionTypes {
  GET_REPORT_LIST = 'Get Report List',
  SET_REPORT_LIST = 'Set Report List',
  GET_REPORT = 'Get Report',
  GET_TITLE = 'Get Title',
  GET_REPORT_SUCCESS = 'Get Report Success',
  GET_REPORT_FIELDS_SUCCESS = 'Get Report Fields Success',
  GET_FIELDS = 'Get Fields',
  GET_FIELDS_SUCCESS = 'Get Fields Success',
  GET_RELATED_FIELDS = 'Get Related Fields',
  GET_RELATED_FIELDS_SUCCESS = 'Get Related Fields Success',
  CHANGE_REPORT_DESCRIPTION = 'Change Report Description',
  CHANGE_REPORT_TITLE = 'Change Report Title',
  TOGGLE_REPORT_DISTINCT = 'Toggle Report Distinct',
  DELETE_REPORT = 'Delete Report',
  DELETE_REPORT_SUCCESS = 'Delete Report Success',
  EDIT_REPORT = 'Edit Report',
  EDIT_REPORT_SUCCESS = 'Edit Report Success',
  EDIT_REPORT_FAILURE = 'Edit Report Failure',
  GENERATE_PREVIEW = 'Generate Preview',
  GENERATE_PREVIEW_SUCCESS = 'Generate Preview Success',
  EXPORT_REPORT = 'Export Report',
  CREATE_REPORT = 'Create Report',
  CREATE_REPORT_SUCCESS = 'Create Report Success',
  CREATE_REPORT_ERROR = 'Create Report Error',
  CANCEL_GENERATE_PREVIEW = 'Cancel Generate Preview',
  COPY_REPORT = 'Copy Report',
  DOWNLOAD_EXPORTED_REPORT = 'Download Exported Report',
  CHECK_EXPORT_STATUS = 'Check Export Status',
  CANCEL_EXPORT_REPORT = 'Cancel Export Report',
  TOGGLE_LEFT_NAV = 'Toggle Left Nav',
  SORT_REPORTS = 'Sort Reports',
  TOGGLE_RIGHT_NAV = 'Toggle Right Nav',
  CHANGE_TAB = 'Change Tab',
  ADD_REPORT_FIELD = 'Add Report Field',
  SELECT_FIELD = 'Select Field',
  CHANGE_DISPLAY_FIELD_POSITION = 'Change Display Field Position',
  CHANGE_FILTER_POSITION = 'Change Filter Position',
}

/** Request an updated list of all reports from the api */
export class GetReportList implements Action {
  readonly type = ReportActionTypes.GET_REPORT_LIST;
}

export class SetReportList implements Action {
  readonly type = ReportActionTypes.SET_REPORT_LIST;
  constructor(public payload: IReport[]) {}
}

/** Get the report details for one report for active editing */
export class GetReport implements Action {
  readonly type = ReportActionTypes.GET_REPORT;
  constructor(public payload: number) {}
}

export class GetTitle implements Action {
  readonly type = ReportActionTypes.GET_TITLE;
  constructor(public payload: string) {}
}

export class GetReportSuccess implements Action {
  readonly type = ReportActionTypes.GET_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class GetReportFieldsSuccess implements Action {
  readonly type = ReportActionTypes.GET_REPORT_FIELDS_SUCCESS;
  constructor(
    public payload: { relatedFields: IRelatedField[]; fields: IField[] }
  ) {}
}

export class GetFields implements Action {
  readonly type = ReportActionTypes.GET_FIELDS;
  constructor(public payload: IRelatedField) {}
}

export class GetFieldsSuccess implements Action {
  readonly type = ReportActionTypes.GET_FIELDS_SUCCESS;
  constructor(public payload: IField[]) {}
}

export class GetRelatedFields implements Action {
  readonly type = ReportActionTypes.GET_RELATED_FIELDS;
  constructor(public payload: INestedRelatedField) {}
}

export class GetRelatedFieldsSuccess implements Action {
  readonly type = ReportActionTypes.GET_RELATED_FIELDS_SUCCESS;
  constructor(
    public payload: {
      parentId: number;
      relatedFields: IRelatedField[];
    }
  ) {}
}

export class ChangeReportDescription implements Action {
  readonly type = ReportActionTypes.CHANGE_REPORT_DESCRIPTION;
  constructor(public payload: string) {}
}

export class ChangeReportTitle implements Action {
  readonly type = ReportActionTypes.CHANGE_REPORT_TITLE;
  constructor(public payload: string) {}
}

export class ToggleReportDistinct implements Action {
  readonly type = ReportActionTypes.TOGGLE_REPORT_DISTINCT;
  constructor(public payload?: boolean) {}
}

export class DeleteReport implements Action {
  readonly type = ReportActionTypes.DELETE_REPORT;
  constructor(public payload: number) {}
}

export class DeleteReportSuccess implements Action {
  readonly type = ReportActionTypes.DELETE_REPORT_SUCCESS;
  constructor(public reportId: number) {}
}

export class EditReport implements Action {
  readonly type = ReportActionTypes.EDIT_REPORT;
  constructor() {}
}

export class EditReportSuccess implements Action {
  readonly type = ReportActionTypes.EDIT_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class EditReportFailure implements Action {
  readonly type = ReportActionTypes.EDIT_REPORT_FAILURE;
  constructor(public payload: IReportErrors) {}
}

export class GeneratePreview implements Action {
  readonly type = ReportActionTypes.GENERATE_PREVIEW;
  constructor() {}
}

export class GeneratePreviewSuccess implements Action {
  readonly type = ReportActionTypes.GENERATE_PREVIEW_SUCCESS;
  constructor(public payload: IReportPreview) {}
}

export class CancelGeneratePreview implements Action {
  readonly type = ReportActionTypes.CANCEL_GENERATE_PREVIEW;
}

export class ExportReport implements Action {
  readonly type = ReportActionTypes.EXPORT_REPORT;
  constructor(public payload: IExportType) {}
}

export class DownloadExportedReport implements Action {
  readonly type = ReportActionTypes.DOWNLOAD_EXPORTED_REPORT;
  constructor(public payload: string) {}
}

export class CheckExportStatus implements Action {
  readonly type = ReportActionTypes.CHECK_EXPORT_STATUS;
  constructor(public payload: { reportId: string | number; taskId: string }) {}
}

export class CancelExportReport implements Action {
  readonly type = ReportActionTypes.CANCEL_EXPORT_REPORT;
}

export class CreateReport implements Action {
  readonly type = ReportActionTypes.CREATE_REPORT;
  constructor(public payload: INewReport) {}
}

export class CreateReportSuccess implements Action {
  readonly type = ReportActionTypes.CREATE_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export class CreateReportError implements Action {
  readonly type = ReportActionTypes.CREATE_REPORT_ERROR
  constructor(public payload: any) {}
}

export class CopyReport implements Action {
  readonly type = ReportActionTypes.COPY_REPORT;
  constructor(public payload: number) {}
}

export class ToggleRightNav implements Action {
  readonly type = ReportActionTypes.TOGGLE_RIGHT_NAV;
  constructor(public payload?: boolean) {}
}

export class SortReports implements Action {
  readonly type = ReportActionTypes.SORT_REPORTS;
  constructor(public payload: string) {}
}

export class ChangeTab implements Action {
  readonly type = ReportActionTypes.CHANGE_TAB;
  constructor(public payload: number) {}
}

export class AddReportField implements Action {
  readonly type = ReportActionTypes.ADD_REPORT_FIELD;
  constructor(public payload: IBase) {}
}

export class SelectField implements Action {
  readonly type = ReportActionTypes.SELECT_FIELD;
  constructor(public payload: IField) {}
}

export type ReportActions =
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
  | ChangeReportTitle
  | ToggleReportDistinct
  | DeleteReport
  | DeleteReportSuccess
  | EditReport
  | EditReportSuccess
  | EditReportFailure
  | GeneratePreview
  | GeneratePreviewSuccess
  | ExportReport
  | CancelExportReport
  | CancelGeneratePreview
  | CreateReport
  | CreateReportSuccess
  | CreateReportError
  | CopyReport
  | DownloadExportedReport
  | CheckExportStatus
  | SortReports
  | ToggleRightNav
  | SortReports
  | ChangeTab
  | AddReportField
  | SelectField;
