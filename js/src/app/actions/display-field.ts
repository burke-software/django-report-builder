import { Action } from '@ngrx/store';
import { IDisplayField } from '../api.interfaces';

export enum DisplayFieldActionTypes {
  ADD_ONE = '[Display Fields] Add One',
  UPDATE_ONE = '[Display Fields] Update One',
  DELETE_ONE = '[Display Fields] Delete One'
}

export class AddOne implements Action {
  readonly type = DisplayFieldActionTypes.ADD_ONE;
  constructor(public payload: IDisplayField) {}
}

export type DisplayFieldActions = AddOne;
