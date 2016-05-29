'use strict';

import React from 'react';
import ReactDOM from 'react-dom';
import FacebookLogin from './components/facebook_login/facebook';

var $ = require('jquery');

const responseFacebook = (response) => {
  console.log(response);
  console.log(response["id"]);
  /*
  TODO
  ajax POST to server the user
   */
}

/*
  jquery area for components/divs get/post server
 */

var Content = React.createClass({
  render: function() {
    return (
        <div>
          <FacebookLogin
            appId="361217287335942"
            autoLoad={true}
            callback={responseFacebook}
            icon="fa-facebook" />

            <div id="test">
                <p>
                    test from index.js file
                </p>
            </div>

        </div>
    );
  }
});



ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
