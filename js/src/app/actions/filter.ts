import { Action } from '@ngrx/store';
import { Update } from '@ngrx/entity';
import { IFilter } from '../models/api';

export enum FilterActionTypes {
  LOAD_ALL = '[Filters] Load All',
  UPDATE_ONE = '[Filters] Update One',
  UPDATE_MANY = '[Filters] Update Many',
  DELETE_ONE = '[Filters] Delete One',
}

export class LoadAll implements Action {
  readonly type = FilterActionTypes.LOAD_ALL;
  constructor(public payload: IFilter[]) {}
}

export class UpdateOne implements Action {
  readonly type = FilterActionTypes.UPDATE_ONE;
  constructor(public payload: Update<IFilter>) {}
}

export class UpdateMany implements Action {
  readonly type = FilterActionTypes.UPDATE_MANY;
  constructor(public payload: Update<IFilter>[]) {}
}

export class DeleteOne implements Action {
  readonly type = FilterActionTypes.DELETE_ONE;
  constructor(public payload: number) {}
}

export type FilterActions = LoadAll | UpdateOne | UpdateMany | DeleteOne;
