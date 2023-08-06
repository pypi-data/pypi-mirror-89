import { actions } from 'actions/hardwareInfoActions';

const hardwareInfoReducer = (state = {}, action: Record<string, any>) => {
  switch (action.type) {
    case actions.FETCH_REQUEST:
      return {
        ...state,
        [action.payload.tabIndex]: {
          isLoading: true,
        },
      };
    case actions.FETCH_SUCCESS:
      return {
        ...state,
        [action.payload.tabIndex]: {
          isLoading: false,
          error: '',
          ...action.payload,
        },
      };
    case actions.FETCH_FAILURE:
      return {
        ...state,
        [action.payload.tabIndex]: {
          isLoading: false,
          data: {},
          ...action.payload,
        },
      };
    default:
      return state;
  }
};

export default hardwareInfoReducer;
