import { Action } from '@ngrx/store';
import { IReport } from '../api.interfaces';

export const GET_REPORT_LIST = 'Get Report List';
export const SET_REPORT_LIST = 'Set Report List';

/** Request an updated list of all reports from the api */
export class GetReportList implements Action {
    readonly type = GET_REPORT_LIST;
}

export class SetReportList implements Action {
    readonly type = SET_REPORT_LIST;

    constructor(public payload: IReport[]) {}
}

export type Actions = GetReportList | SetReportList;
