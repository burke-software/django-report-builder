import * as configActions from '../actions/config';
import { State } from '../models/config';

export function reducer(state = {}, action: configActions.Actions): State {
  switch (action.type) {
    case configActions.GET_CONFIG_SUCCESS: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
