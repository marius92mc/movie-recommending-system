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
  } /* if */
}

/*
  jquery area for components/divs get/post server
 */

var gMoviesName = [
];

$(document).ready(function() {
  $.ajax({
    type: "GET",
    url: Flask.url_for("get_movies"),
    data: "",
    contentType: 'application/json;charset=UTF-8',
    success: function (movie_entries) {
      var parsed = JSON.parse(movie_entries);
      for (var i = 0; i < parsed.length; i++) {
        gMoviesName.push(parsed[i]["name"]);
      }
      console.log("Autocomplete populated with " + gMoviesName.length + " movie titles");
    }
  }); /* ajax */
});



var Content = React.createClass({
  render: function() {
    return (
        <div>
          <FacebookLogin
            appId="361217287335942"
            autoLoad={true}
            callback={responseFacebook}
            icon="fa-facebook" />

            <Autocomplete
              placeholder="Enter a movie title..."
              data={ gMoviesName } />

        </div>
    );
  }
});



ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
