import React, {Component} from 'react';
import { Route, Switch, withRouter, Redirect } from 'react-router-dom';
import Layout from './hoc/Layout/Layout';
import PITMainPanel from './containers/PITMainPanel/PITMainPanel';
import Auth from './containers/Auth/Auth';
import axios from 'axios';

class App extends Component {


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

  return (
    <div>
      <Layout>
        {routes}
      </Layout>
    </div>
  );
}
}

export default App;
