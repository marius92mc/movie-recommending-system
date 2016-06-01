'use strict';

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import FacebookLogin from './components/facebook_login/facebook';
import Autocomplete from './components/autocomplete/autocomplete';
import Rating from './components/star_rating/star_rating';

var $ = require('jquery');

var gLoggedInUserId = "";

const responseFacebook = (response) => {
  console.log(response);
  console.log(response["id"]);

  if ('id' in response &&
      'name' in response &&
      'accessToken' in response) {

    console.log("logged in user, all the fields present");
    gLoggedInUserId = response["id"];

    /*
     * POSTing the logged in user's data
     */
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
  /*
   * Populating autocomplete with movie names
   */
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
  }); /* ajax GET */
});


var RateMovie = React.createClass({
  getInitialState: function() {
    return {
      movieName: '',
      rating: this.props.starCount
    }
  },

  componentDidMount: function() {
    $("#loadingImage").hide();
  },

  changeInputMovieName: function(movieName) {
    this.setState({
      movieName: movieName
    });
  },

  changeInputRating: function(ratingClicked) {
    this.setState({
      rating: ratingClicked
    });
  },

  handleSubmit: function(e) {
    if (gLoggedInUserId == "") {
      alert("Please log in first");
      return ;
    }

    $("#retrainedMessage").html("Training...");

    /*
     * POST movieName and rating to server
     */
    $.ajax({
      type: "POST",
      url: Flask.url_for("add_rating", { "user_id": gLoggedInUserId }),
      data: JSON.stringify(this.state, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      beforeSend: function() {
        $("#loadingImage").show();
      },
      success: function (result) {
        console.log(result);
        $("#loadingImage").hide();
        $("#retrainedMessage").html("Trained in " + result + ' seconds.');
      }
    }); /* ajax */

    console.log(this.state);
  },

  render: function() {
    let boundClick = this.handleSubmit;

    return (
      <div>

        <Autocomplete
          placeholder={ this.props.autocompletePlaceholder }
          data={ this.props.autocompleteData }
          onSelect={ this.changeInputMovieName } />

        <Rating
          starCount = { this.props.starCount }
          onSelect={ this.changeInputRating }/>

        <div onClick={ boundClick }>Click me</div>
        <img id="loadingImage" src="../../static/images/ring-alt.gif" />
        <div id="retrainedMessage"> </div>

      </div>
    );
  }
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

          <RateMovie
            autocompletePlaceholder="Enter a movie title..."
            autocompleteData = { gMoviesName }
            starCount = { 10 } />

        </div>
    );
  }
});



ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
