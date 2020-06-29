import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actions from '../../store/actions/index';

class Logout extends Component {

    componentDidMount () {
        this.props.onLogout();
    }

    render () {
        console.log("logout hit");
        return (
        <div>
            <Redirect to="/"/>
        </div> );
            
        
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onLogout: () => dispatch(actions.appLogout())
    };
};

export default connect(null, mapDispatchToProps)(Logout);