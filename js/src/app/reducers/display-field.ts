import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';

import { DisplayFieldActions, DisplayFieldActionTypes } from '../actions/display-field';
import { IDisplayField } from '../api.interfaces';

export interface State extends EntityState<IDisplayField> {}

export const adapter: EntityAdapter<IDisplayField> = createEntityAdapter<IDisplayField>();

const initialState: State = adapter.getInitialState();

export function reducer(
  state: State = initialState,
  action: DisplayFieldActions,
): State {
  switch (action.type) {
    case DisplayFieldActionTypes.ADD_ONE:
      return adapter.addOne(action.payload, state);

    default:
      return state;
  }
}

export const {
  selectIds,
  selectEntities,
  selectAll,
  selectTotal,
} = adapter.getSelectors();
