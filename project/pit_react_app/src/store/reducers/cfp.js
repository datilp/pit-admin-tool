import { QUERY_CFP, ADD_CFP, UPDATE_CFP, SET_STATE_CFP } from '../actions/actionTypes';

const initialState = {
    currentSem: {open:null, close:null, tz:null, idx:-1},
    semList: [],
};


export default function (state = initialState, action) {
    switch(action.type) {
        case QUERY_CFP:
            // set the idx on currentSem after a query has been made

            // if currentSem has id means it's also in the semList
            if (action.payload.currentSem.id) {
                let cfp = action.payload.semList.find( e => e.semester.id)
            }
            //action.payload.currentSem.idx = action.payload.semList.length;
            return {
                ...state,
                ...action.payload
            };
        case ADD_CFP:
            return {
                ...state,
                cfps: [...state.cfps, action.payload],
            };
        case UPDATE_CFP:
            console.log("UPDATE_CFP:", action.payload);

            return {
                ...state,
                currentSem: {
                    // This is just so the idx index
                    // is added to currentSem
                    ...state.currentSem,
                    ...action.payload
                }
            };
        case SET_STATE_CFP:
            console.log("SET_STATE_CFP:", action.payload);
            return {
                ...state,
                ...action.payload
            };
        default:
                return state;

    }

}