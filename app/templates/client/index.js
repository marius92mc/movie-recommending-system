'use strict';

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import FacebookLogin from './components/facebook_login/facebook';
import Autocomplete from './components/autocomplete/autocomplete';

var $ = require('jquery');

const responseFacebook = (response) => {
  console.log(response);
  console.log(response["id"]);

  if ('id' in response &&
      'name' in response &&
      'accessToken' in response) {
    console.log("logged in user, all the fields present");

    $.ajax({
      type: "POST",
      url: Flask.url_for("save_user", {/* "param1": 1, "param2": "text" */}), // the method name, see the response from http://stackoverflow.com/questions/10314800/flask-url-for-urls-in-javascript
      data: JSON.stringify(response, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function (result) {
        console.log(result);
      }
    });
  } else {
    console.log("logged in user doesn't have the required fields")
  }

}

/*
  jquery area for components/divs get/post server
 */

const data = [
    'phrase one',
    'phrase two'
];


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

            <Autocomplete
              placeholder="Enter a movie title..."
              data={ data } />

        </div>
    );
  }
});



ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
