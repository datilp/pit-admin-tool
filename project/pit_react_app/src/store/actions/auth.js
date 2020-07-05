import * as actionTypes from './actionTypes';
import axios from 'axios';

/* ################################################# */
/* ###########    Action Dispatchers   ############# */
/* ################################################# */

// The authentication will be done to some backend server
// This action distpatches the state that says we are 
// sending the data to the server and we are waiting.
// We are using this to run a spinner for instance.
export const authStart = () => {
    return {
        type: actionTypes.AUTH_START
    };
};

export const authSuccess = (token, userId) => {
    return {
        type: actionTypes.AUTH_SUCCESS,
        idToken: token,
        userId: userId
    };
};

export const authFail = (error) => {
    return {
        type: actionTypes.AUTH_FAIL,
        error: error
    };
};

export const setAuthRedirectPath = (path) => {
    return {
        type: actionTypes.REDIRECT_PATH_AFTER_AUTH,
        path: path
    };
};

export const logout = () => {
    console.log("deleting localstorage");
    localStorage.removeItem('token');
    localStorage.removeItem('expirationDate');
    localStorage.removeItem('userId');
    return {
        type: actionTypes.AUTH_LOGOUT
    };
};


// convinience action dispatcher. It sets the path you want to go
// 
export const setRedirectPathAfterAuth = (path) => {
    return {
        type: actionTypes.REDIRECT_PATH_AFTER_AUTH,
        path: path
    };
};

// When we log in, the backend server will give us an expiration
// time, after which the user will automatically logged out.
export const checkAuthTimeout = (expirationTime) => {
    return dispatch => {
        setTimeout(() => {
            dispatch(logout());
        }, expirationTime * 1000);
    };
};

/* ################################################# */
/* ###########     Action Creators     ############# */
/* ################################################# */

export const auth = (email, password) => {
    return dispatch => {
        dispatch(authStart());
        
        // I'm using the knox authenticantion and at the time of writing the way of 
        // passing that down is via the Authorization header with the keyword Basic
        // follow with space and the email:password encoded in base64.
        // The reason for the encoding is simply to make things more dificult to hackers
        // in case the email/password combination goes out in the open.
        const encodedAuthData = new Buffer(email+":"+password).toString('base64');
        console.log("encodeAuthData:"+encodedAuthData);


        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + encodedAuthData
                }
        };
    

        let url = "http://localhost:8000/api/user/loginx/";
        
        axios.post(url, null, config)
            .then(response => {
                console.log(response)
                // we use local storage, a browser API to store data that survive
                // a page refresh.
                // the redux storage works as long as the page is not refreshed but
                // once it is all the state is lost as it is just javascript objects.
                // so we store the localstorage here before dispatching to the reducer.
                // We could have done it in the action dispatcher but there is no point 
                // of passing the expiration time there, since it doesn't survive a refresh.
                // So here in the action creator looks like the right place to put it.
                localStorage.setItem('token', response.data.token);

                // new Date with argument is an object with the date we are passing in
                // Date without argument is the current datetime.

                const expirationDate = new Date(new Date().getTime() +  response.data.expirationTime * 1000);
                

                localStorage.setItem('expirationDate', expirationDate);
                localStorage.setItem('userId', response.data.userId);
                dispatch(authSuccess(response.data.token, response.data.userId));
                dispatch(checkAuthTimeout(response.data.expirationTime))
            })
            .catch(err => {
                dispatch(authFail(err.response.data.error))
            })

       
       
    };
};

export const appLogout = () => {
    let url = "http://localhost:8000/api/user/logoutx/";

    return dispatch => {
        const token = localStorage.getItem('token');
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
                }
        };
    
        if (!token) {
            console.log("There is no token");
            dispatch(logout());
        } else {
            axios.post(url,null, config)
            .then((res) => {
                dispatch(logout())
                console.log("logout successful");
            }).catch((err) => {
                console.log(err.response.data.error);
                dispatch(logout());
                dispatch(authFail(err.response.data.error));
            })
        }
    };
};

// checks if the current authorization is still valid
// this method is typically called from either a lifecycle hook
// (e.g. componentDidMount) that allows side effects, such as back 
// server calls or from an event triggering function, such as clicking
// a submit button.
export const authCheckState = () => {
    return dispatch => {
        const token = localStorage.getItem('token');
        if (!token) {
            dispatch(logout());
        } else {
            const expirationDate = new Date(localStorage.getItem('expirationDate'));
            if (expirationDate <= new Date()) {
                dispatch(logout());
            } else {
                // TODO
                // Ideally we might want to get the userId from the backend server
                // say that via another way the user deletes the account, this will 
                // be a good way to keep that in sync.
                const userId = localStorage.getItem('userId');
                dispatch(authSuccess(token, userId));
                // getTime() gets the time in milliseconds since epoch, and the
                // checkAuthTimeout is in seconds so we divide by 1000
                dispatch(checkAuthTimeout((expirationDate.getTime() - new Date().getTime()) / 1000 ));
            }   
        }
    };
};
