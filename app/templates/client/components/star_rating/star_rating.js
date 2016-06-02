import React from 'react';

var Star = React.createClass({
	render: function() {
	    var r = 'fa fa-star';
    	if(!this.props.selected){
          r += '-o';
        }
        return (
        	<i {...this.props} className={ r }/>
        );
    }
});

var Rating = React.createClass({
	getInitialState: function(){
    return {
      rating: this.props.starCount,
      hoverAt: null
    };
  },

  handleMouseOver: function(idx, evt){
    this.state.hoverAt = idx + 1;
    this.forceUpdate();
  },

  handleMouseOut: function(idx, evt){
    this.state.hoverAt = null;
    this.forceUpdate();
  },

  handleClick: function(idx, evt){
    this.state.rating = idx + 1;
    this.forceUpdate();
    console.log('clicked ' + this.state.rating);
    this.props.onSelect(this.state.rating);
  },

	render: function(){
    var stars = [];

    for (var i = 0; i < this.props.starCount; i++) {
      var rating = (this.state.hoverAt != null)? (this.state.hoverAt): (this.state.rating);
      var selected = (i < rating);
      stars.push(
        <Star
          key={ i }
          selected={ selected }
          onMouseOver={ this.handleMouseOver.bind(this, i) }
          onMouseOut={ this.handleMouseOut.bind(this, i) }
          onClick={ this.handleClick.bind(this, i) }
        />);
    }

    return (<div>{stars}</div>);
  }
});

export default Rating;
