'use strict';

import React from 'react';
import ReactDOM from 'react-dom';
import FacebookLogin from './components/facebook_login/facebook';

var $ = require('jquery');

const responseFacebook = (response) => {
  console.log(response);
  console.log(response["id"]);
  /*
  $('#facebook_login').hide( "slow", function() {
    alert("Animation complete.");
  });
  */
}

var Content = React.createClass({
  render: function() {
    return (
        <div>
          <FacebookLogin
            appId="361217287335942"
            id="facebook_login"
            autoLoad={true}
            callback={responseFacebook}
            icon="fa-facebook" />

            <div id="mere">
                mere from index.js file
            </div>
        </div>
    );
  }
});

ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
/*
ReactDOM.render(
  <FacebookLogin
    appId="361217287335942"
    id="facebook_login"
    autoLoad={true}
    callback={responseFacebook}
    icon="fa-facebook" />,
  document.getElementById('demo')
);
*/