import { Action } from '@ngrx/store';
import { IReport, IReportDetailed } from '../api.interfaces';

export const GET_REPORT_LIST = 'Get Report List';
export const SET_REPORT_LIST = 'Set Report List';
export const GET_REPORT = 'Get Report';
export const GET_REPORT_SUCCESS = 'Get Report Success';

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

export type Actions = GetReportList
  | SetReportList
  | GetReport
  | GetReportSuccess;
