import { Action } from '@ngrx/store';
import { Update } from '@ngrx/entity';
import { IDisplayField } from '../api.interfaces';

export enum DisplayFieldActionTypes {
  LOAD_ALL = '[Display Fields] Load All',
  ADD_ONE = '[Display Fields] Add One',
  UPDATE_ONE = '[Display Fields] Update One',
  UPDATE_MANY = '[Display Fields] Update Many',
  DELETE_ONE = '[Display Fields] Delete One',
}

export class LoadAll implements Action {
  readonly type = DisplayFieldActionTypes.LOAD_ALL;
  constructor(public payload: IDisplayField[]) {}
}

export class AddOne implements Action {
  readonly type = DisplayFieldActionTypes.ADD_ONE;
  constructor(public payload: IDisplayField) {}
}

export class UpdateOne implements Action {
  readonly type = DisplayFieldActionTypes.UPDATE_ONE;
  constructor(public payload: Update<IDisplayField>) {}
}

export class UpdateMany implements Action {
  readonly type = DisplayFieldActionTypes.UPDATE_MANY;
  constructor(public payload: Update<IDisplayField>[]) {}
}

export class DeleteOne implements Action {
  readonly type = DisplayFieldActionTypes.DELETE_ONE;
  constructor(public payload: number) {}
}

export type DisplayFieldActions =
  | LoadAll
  | AddOne
  | UpdateOne
  | UpdateMany
  | DeleteOne;
