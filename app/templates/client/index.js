'use strict';

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import FacebookLogin from './components/facebook_login/facebook';
import Autocomplete from './components/autocomplete/autocomplete';
import Rating from './components/star_rating/star_rating';
import Center from 'react-center';
import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// Check this repo:
// https://github.com/zilverline/react-tap-event-plugin
injectTapEventPlugin();
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

import ReactDataGridExample from './components/react_data_grid_example/react_data_grid_example';

var $ = require('jquery');

var gLoggedInUserId = "";
var gRecommendedMovies = [];


function getBestRecommendations() {
  gRecommendedMovies = [];
  $("#bestRecommendations").html("");
  //$("#bestRecommendations").html("Computing...");

  /*
   * GETing best recommendations
   */
  $.ajax({
    type: "GET",
    url: Flask.url_for("get_best_ratings", { "user_id": gLoggedInUserId, "num_movies": 200 }),
    data: "",
    contentType: 'application/json;charset=UTF-8',
    beforeSend: function() {
        $("#loadingImage3").show();
    },
    success: function (movies) {
      var parsed = JSON.parse(movies);
      for (var i = 0; i < parsed.length; i++) {
        gRecommendedMovies.push(parsed[i]);
      }
      $("#loadingImage3").hide();
      console.log(gRecommendedMovies);
      if (gRecommendedMovies.length > 0) {
        console.log(gRecommendedMovies[0]);
      }
      console.log("Populated with " + gRecommendedMovies.length + " movies");

      $("#bestRecommendations").append("<ul class='list-group'>");
      for (var i = 0; i < 10; i++) {
        $("#bestRecommendations").append("<li class='list-group-item'>" +
                                            "<span class='badge'>" +
                                               gRecommendedMovies[i][1].toFixed(2) +
                                            "</span>" +
                                            (i + 1) + ". " +
                                            gRecommendedMovies[i][0] +
                                         "</li>");
      }
       $("#bestRecommendations").append("</ul>");

    }
  }); /* ajax GET */
}


function loadBodyBackgroundImage(numMiliseconds) {
  setTimeout(function() {
      $('body').css("background-image", "url(http://marius92mc.github.io/materials/images/connections.jpg)")
    },
    numMiliseconds
  );
}


function makeBackgroundGrey() {
  $('body').css('background', '#EEEEEE');
}


$(window).load(function() {
  loadBodyBackgroundImage(0);
});


const responseFacebook = (response) => {
  if (response == null) {
    $("#predictedMovie").hide();
    $("#retrainedMessage").hide();

    $("#information").hide(1500);
    loadBodyBackgroundImage(1300);

    console.log("logged in user doesn't have the required fields");
    return false;
  }
  console.log(response);
  console.log(response["id"]);

  if ('id' in response &&
      'name' in response &&
      'accessToken' in response) {

    makeBackgroundGrey();
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

    $("#information").show(1500);

    getBestRecommendations();
  } /* if */

  return true;
}

/*
  jquery area for components/divs get/post server
 */

var gMoviesName = [];


$(document).ready(function() {
  $("#information").hide();

  /*
   * Populating autocomplete with movie names
   */
  $.ajax({
    type: "GET",
    url: Flask.url_for("get_movies"),
    data: "",
    contentType: 'application/json;charset=UTF-8',
    success: function(movieEntries) {
      var parsed = JSON.parse(movieEntries);

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
    $("#retrainedMessage").show();
    $("#retrainedMessage").html("<i><small>Training...</small></i>");

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
        $("#retrainedMessage").html("<i><small>Trained in " + result + ' seconds.</small></i>');

        getBestRecommendations();

        $("#retrainedMessage").delay(5000).fadeOut('slow');
      }
    }); /* ajax */

    console.log(this.state);
  },

  render: function() {
    return (
      <div>

        <Autocomplete
          placeholder={ this.props.autocompletePlaceholder }
          data={ this.props.autocompleteData }
          onSelect={ this.changeInputMovieName } />

        <Rating
          starCount = { this.props.starCount }
          onSelect={ this.changeInputRating }/>

        <MuiThemeProvider muiTheme={getMuiTheme()}>
          <FlatButton
            label="Rate"
            primary={ true }
            onTouchTap={ this.handleSubmit }
            style={{
              position: 'static',
              margin: '0 auto'
            }} />
        </MuiThemeProvider>

        <img id="loadingImage" src="../../static/images/ring-alt.gif" />
        <div id="retrainedMessage"> </div>

      </div>
    );
  }
});


var BestRecommendations = React.createClass({
  getInitialState: function() {
    return null; /* TODO put data from gRecommendedMovies, is already filled */
  },

  componentDidMount: function() {
    $("#loadingImage3").hide();
  },

  render: function() {
    return (
      <div>
        <center>
          <div>
              <b>
                Recommended Movies
              </b>
          </div>
          <img id="loadingImage3" src="../../static/images/ring-alt.gif" />
        </center>
        <div id="bestRecommendations"> </div>
      </div>
    );
  }
});


var PredictMovieRating = React.createClass({
  getInitialState: function() {
    return {
      movieName: ''
    }
  },

  componentDidMount: function() {
    $("#loadingImage2").hide();
  },

  changeInputMovieName: function(movieName) {
    this.setState({
      movieName: movieName
    });
  },

  handleSubmit: function(e) {
    if (gLoggedInUserId == "") {
      alert("Please log in first");
      return;
    }

    $("#predictedMovie").show();
    $("#predictedMovie").html("<center> " +
                                "<i>" +
                                  "<small>" +
                                    "Computing..." +
                                  "</small>" +
                                "</i>" +
                              "</center>");

    /*
     * POST movieName to server
     */
    $.ajax({
      type: "POST",
      url: Flask.url_for("get_predicted_movie_rating", {
        "user_id": gLoggedInUserId,
      }),
      data: JSON.stringify(this.state, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      beforeSend: function() {
        $("#loadingImage2").show();
      },
      success: function (predictedMovie) {
        predictedMovie = JSON.parse(predictedMovie);
        console.log(predictedMovie);
        $("#loadingImage2").hide();
        $("#predictedMovie").show(1500);

        $("#predictedMovie").html("");
        $("#predictedMovie").append("<ul class='list-group'>" +
                                       "<li class='list-group-item'>" +
                                          "<span class='badge'>" +
                                            predictedMovie['rating'].toFixed(2) +
                                          "</span>" +
                                          predictedMovie['movieName'] +
                                       "</li>" +
                                    "</ul>");
        $("#predictedMovie").delay(9000).fadeOut('slow');
      }
    }); /* ajax */
  },

  render: function() {
    return (
      <div>
        <center>
          <div>
              <b>
                Predict Rating
              </b>
          </div>

          <br />

          <Autocomplete
            placeholder={ this.props.autocompletePlaceholder }
            data={ this.props.autocompleteData }
            onSelect={ this.changeInputMovieName } />

          <MuiThemeProvider muiTheme={getMuiTheme()}>
            <FlatButton
              label="Submit"
              primary={ true }
              onTouchTap={ this.handleSubmit }
              style={{
                position: 'static',
                margin: '0 auto'
              }} />
          </MuiThemeProvider>

          <img id="loadingImage2" src="../../static/images/ring-alt.gif" />
        </center>

        <br /> <br />
        <div id="predictedMovie"> </div>
        <br /> <br /> <br /> <br /> <br /> <br />

      </div>
    );
  }
});


var Content = React.createClass({
  render: function() {
    return (
        <div class="container">

          <FacebookLogin
            appId="361217287335942"
            autoLoad={true}
            callback={responseFacebook}
            icon="fa-facebook" />

          <br /> <br />

          <Center>
            <div id="information">
              <center>
              <RateMovie
                autocompletePlaceholder="Enter a movie title..."
                autocompleteData={ gMoviesName }
                starCount={ 10 } />
              </center>

              <br />
              <BestRecommendations />
              <br /> <br /> <br />

              <PredictMovieRating
                autocompletePlaceholder="Enter a movie title..."
                autocompleteData={ gMoviesName } />
            </div>
          </Center>

        </div>
    );
  }
});




ReactDOM.render(
    <Content />,
    document.getElementById('demo')
);
