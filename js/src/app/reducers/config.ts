import { Actions, ConfigActionTypes } from '../actions/config';
import { State } from '../models/config';

export function reducer(state = {}, action: Actions): State {
  switch (action.type) {
    case ConfigActionTypes.GET_CONFIG_SUCCESS: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
