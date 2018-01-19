import { Action } from '@ngrx/store';
import {
  IReport,
  IReportDetailed,
  IRelatedField,
  IField
} from '../api.interfaces';

export const GET_REPORT_LIST = 'Get Report List';
export const SET_REPORT_LIST = 'Set Report List';
export const GET_REPORT = 'Get Report';
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
  constructor(public payload: number) {}
}

export class DeleteReportSuccess implements Action {
  readonly type = DELETE_REPORT_SUCCESS;
  constructor() {}
}

export class EditReport implements Action {
  readonly type = EDIT_REPORT;
  constructor() {}
}

export class EditReportSuccess implements Action {
  readonly type = EDIT_REPORT_SUCCESS;
  constructor(public payload: IReportDetailed) {}
}

export type Actions =
  | GetReportList
  | GetReportFieldsSuccess
  | SetReportList
  | GetReport
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
  | EditReportSuccess;
