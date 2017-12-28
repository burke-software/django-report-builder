import { Action } from '@ngrx/store';
import {
    IReport,
    IReportDetailed,
    IRelatedField,
    IField,
} from '../api.interfaces';

export const GET_REPORT_LIST = 'Get Report List';
export const SET_REPORT_LIST = 'Set Report List';
export const GET_REPORT = 'Get Report';
export const GET_REPORT_SUCCESS = 'Get Report Success';
export const GET_REPORT_FIELDS_SUCCESS = 'Get Report Fields Success';
export const GET_FIELDS = 'Get Fields';
export const GET_FIELDS_SUCCESS = 'Get Fields Success';

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
    constructor(public payload: {relatedFields: IRelatedField[], fields: IField[]}) {}
}

export class GetFields implements Action {
    readonly type = GET_FIELDS;
    constructor(public payload: IRelatedField) {}
}

export class GetFieldsSuccess implements Action {
    readonly type = GET_FIELDS_SUCCESS;
    constructor(public payload: IField[]) {}
}

export type Actions = GetReportList
  | GetReportFieldsSuccess
  | SetReportList
  | GetReport
  | GetReportSuccess
  | GetFields
  | GetFieldsSuccess;
