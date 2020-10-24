import * as actionTypes from './actionTypes';
import axios from 'axios';
import moment from 'moment';

const DATE_FORMAT="YYYY-MM-DDThh:mm:ssZ";
/* ################################################# */
/* ###########    Action Dispatchers   ############# */
/* ################################################# */

// Several actions are needed for Call for Proposals
// Querying existing CfP
// Creating a new CfP
// Updating a new CfP

export const cfpSending = (token, userId, semesterId) => {
    return {
        type: actionTypes.CFP_SENDING,
        idToken: token,
        userId: userId,
        semesterId: semesterId
    };
}

export const cfpSuccess = (token, userId, semesterId) => {
    return {
        type: actionTypes.CFP_SUCCESS,
        idToken: token
    };
}

// Query success
export const cfpQSuccess = (payload) => {
    return {
        type: actionTypes.QUERY_CFP,
        payload: payload
    };
}

export const cfpFail = (error) => {
    return {
        type: actionTypes.CFP_FAIL,
        error: error
    };
};

export const cfpAddSuccess = (state) => {
    return {
        type: actionTypes.ADD_CFP,
        payload: state
    }
}

export const cfpUpdateSuccess = (state) => {
    return {
        type: actionTypes.UPDATE_CFP,
        payload: state
    }
}

export const cfpSetState = (state) => {
    return {
        type: actionTypes.SET_STATE_CFP,
        payload: state
    }
}


/* ################################################# */
/* ###########     Action Creators     ############# */
/* ################################################# */

export const cfpQuery = (queryParams) => {
    return dispatch => {

        //let url = "http://localhost:8000/api/cfp//";
        let url = "http://localhost:8000/api/current_sem/";


        queryParams = { 
            //'semester__year': "2020",
            //'semester__sem': "A",
            'pi__email': 'testuser3@inaf.it'
        }
        

        //queryParams = { 'pi': 3 }

        //axios.post(url, queryParams, getConfig)
        // or
        let config = {"params" : queryParams,
                  ...getConfig()};
        //console.log("cfpQuery:", config);
        axios.get(url, config)
        .then(response => {
            //console.log("Config:",config);
            //const data = response.data.map((e,idx) => {e.idx = idx; return e;})
            console.log("cfpQuery resp:", response.data);
            dispatch(cfpQSuccess(response.data));
        })
    }
}

export const cfpSaveToDB = (cfpState) => {
    return dispatch => {

        //const url = "http://localhost:8000/api/cfp//";

        //const url = "http://localhost:8000/api/save_to_db/";
        let url = "http://localhost:8000/api/current_sem/";


        //console.log("currentSemester:", cfpState.currentSem);
        let queryParams = {
            //'semester__year': cfpState.currentSem.year,
            //'semester__sem': cfpState.currentSem.sem,
            'semester_id': cfpState.currentSem.semester.id,
            'open': moment(cfpState.currentSem.open, DATE_FORMAT).format(DATE_FORMAT),
            'close': moment(cfpState.currentSem.close, DATE_FORMAT).format(DATE_FORMAT),
            'tz': cfpState.currentSem.tz,
            'pi_id': localStorage.getItem('userId')
            //'pi__email': 'testuser3@inaf.it'
        };

        /*queryParams = {"semester_id": "3", "pi_id": "1", "open": "2020-09-16 16:29:35.884703-07:00", 
        "close": "2020-10-10 16:19:35.889898-07:00",
        "tz": "US/Pacific"};*/
        //console.log("saveToDB:", queryParams)

        //queryParams = { 'pi': 3 }

        //axios.post(url, queryParams, getConfig)
        // or
        //let config = {"params" : queryParams,
        //          ...getConfig};
        const config = {...getConfig()};
        //console.log("cfpSaveToDB:",queryParams, config);
        //axios.post(url, queryParams, {'Authorization': `Token ${localStorage.getItem('token')}`})

        // Here we make the decision about if this is a new CfP or an 
        // existing one that needs updating.
        // If it is a new one it'll be a post method, updates is patch
        if (cfpState.currentSem.id) {
            axios.patch(`http://localhost:8000/api/cfp//${cfpState.currentSem.id}/`, queryParams, config)

            //            axios.patch(`http://localhost:8000/api/cfp/${cfpState.currentSem.id}/`, queryParams, config)
            .then(response => {
                console.log("Patch:",response.data);
                dispatch(cfpUpdateSuccess(response.data));
            })
        } else {
            //axios.post(url, queryParams, config)
            axios.post("http://localhost:8000/api/cfp//", queryParams, config)
            .then(response => {
                console.log("Post:", response.data);
                /*
                {
                    "id": 13,
                    "semester": {
                        "id": 13,
                        "year": 2021,
                        "sem": "A"
                    },
                    "pi": {
                        "id": 3,
                        "last_login": "2020-10-22T12:30:44.663634Z",
                        "email": "testuser3@inaf.it",
                        "name": "Test User 3",
                        "partner": "INAF"
                    },
                    "open": "2021-08-31T12:00:00Z",
                    "close": "2021-10-10T12:00:00Z",
                    "tz": "Europe/Rome"
                }
                */
                dispatch(cfpAddSuccess(response.data));
        })
    }
    }
}

// Setup config with token - helper function
// must be a function and not a value. 
// I had it as a value an the token is null, because this is set 
// during construction before we even log in, so the value will
// always be null.
const getConfig = () => {
    return { headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + localStorage.getItem('token')
        }
    };
}
