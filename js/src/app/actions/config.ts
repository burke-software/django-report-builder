import { Action } from '@ngrx/store';
import { IConfig } from '../models/api';

export const GET_CONFIG = 'Get Config';
export const GET_CONFIG_SUCCESS = 'Get Config Success';

export class GetConfig implements Action {
  readonly type = GET_CONFIG;
  constructor() {}
}

export class GetConfigSuccess implements Action {
  readonly type = GET_CONFIG_SUCCESS;
  constructor(public payload: IConfig) {}
}
export type Actions = GetConfig | GetConfigSuccess;
