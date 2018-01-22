import * as configActions from '../actions/config';

export interface State {
  async_report?: boolean;
}

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

export const getIsAsyncReport = (state: State) => state.async_report;
