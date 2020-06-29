import * as actionTypes from './actionTypes';

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
        
        const idToken = "sometoken2347afas98";
        const userId  = "U1234";
        const expirationTime = "1000" //in milliseconds?
        
        // we use local storage, a browser API to store data that survive
        // a page refresh.
        // the redux storage works as long as the page is not refreshed but
        // once it is all the state is lost as it is just javascript objects.
        // so we store the localstorage here before dispatching to the reducer.
        // We could have done it in the action dispatcher but there is no point 
        // of passing the expiration time there, since it doesn't survive a refresh.
        // So here in the action creator looks like the right place to put it.
        localStorage.setItem('token', idToken);

        // new Date with argument is an object with the date we are passing in
        // Date without argument is the current datetime.

        const expirationDate = new Date(new Date().getTime() +  expirationTime * 1000);

        localStorage.setItem('expirationDate', expirationDate);
        localStorage.setItem('userId', userId);
        dispatch(authSuccess(idToken, userId));
       
    };
};

export const appLogout = () => {
    return dispatch => {
        const token = localStorage.getItem('token');
        if (!token) {
            console.log("There is no token");
            dispatch(logout());
        } else {
            const tokenData = {
                token: token,
            };

            console.log("token is ", tokenData);

            dispatch(logout())
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
