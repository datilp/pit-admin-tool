import React, {Component} from 'react';
import { Route, Switch, withRouter, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import AdminProposals from './containers/AdminProposals/AdminProposals';
import CallForProposals from './containers/CallForProposals/CallForProposals';
import Logout from './containers/Auth/Logout';
import Layout from './hoc/Layout/Layout';
import PITMainPanel from './containers/PITMainPanel/PITMainPanel';
import Auth from './containers/Auth/Auth';
import * as actions from './store/actions/index';
import axios from 'axios';

class App extends Component {

  // Sometimes the user can sign up automatically, for instance
  // after a refresh.
  componentDidMount () {
    //Try automatic sign up here
    // In the React world the componentDidMount lifecycle hook happens
    // at the end of that cycle, after the state is set up and the 
    // render method has been fired.
    // In this method we want to do things like interacting with the
    // backend server, which potentially can take time, but since everything
    // has been done there is no wait.
    // However, we don't want to update the state since that "could" trigger
    // a new neverending refresh, unless we want that like in this case.
    // 
    // The page will be build and there won't be any login at that point
    // So the page will display the login page, if the auto sign up works
    // then it should be refresh to display the page the user had previously
    // loaded.
    this.props.onTryAutoSignup();
  }

  render() {
    let url = "http://0.0.0.0:8000/testapi/testapi/";
    axios.post(url, {})
    .then(response => {
      console.log(response);
    })
    .catch(err => {
      console.log(err)
    });
  
    let routes = (
      <Switch>
        <Route path="/" exact component={Auth} />
        <Route path="/" exact component={PITMainPanel} />
      </Switch>
    )

    if ( this.props.isAuthenticated ) {
      routes = (
        <Switch>
          <Route path="/adminProposals" component={AdminProposals} />
          <Route path="/callForProposals" component={CallForProposals} />
          <Route path="/logout" component={Logout} />
          <Route path="/" exact component={PITMainPanel} />
          {/*if non of them match then redirect to root "/"*/}
          <Redirect to="/" />
        </Switch>
      );
    }
  
    return (
      <div>
        <Layout>
          {routes}
        </Layout>
      </div>
    );
  }
}


const mapStateToProps = state => {
  return {
    isAuthenticated: state.auth.token !== null
  };
};

const mapDispatchToProps = dispatch => {
  return {
    onTryAutoSignup: () => dispatch( actions.authCheckState() )
  };
};

export default withRouter( connect( mapStateToProps, mapDispatchToProps )( App ) );