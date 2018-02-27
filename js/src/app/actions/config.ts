import { Action } from '@ngrx/store';
import { IConfig } from '../models/api';

export enum ConfigActionTypes {
  GET_CONFIG = 'Get Config',
  GET_CONFIG_SUCCESS = 'Get Config Success',
}

export class GetConfig implements Action {
  readonly type = ConfigActionTypes.GET_CONFIG;
  constructor() {}
}

export class GetConfigSuccess implements Action {
  readonly type = ConfigActionTypes.GET_CONFIG_SUCCESS;
  constructor(public payload: IConfig) {}
}
export type ConfigActions = GetConfig | GetConfigSuccess;
