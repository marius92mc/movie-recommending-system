import React, { Component } from 'react';
import ReactDataGrid from 'react-data-grid';

var $ = require('jquery');

var columns = [{
  key: 'task',
  name: 'Recommended Movies',
  resizable: true
}];


class ReactDataGridExample extends Component {

  constructor(props) {
    super(props);
    return {data: gRecommendedMovies};
  }

  rowGetter = function(i) {
    return this.state.data[i][0];
  }

  /*
  rowGetter = function(i) {
    return _rows[i];
  }
  */

  render() {
    return (
      <ReactDataGrid
        columns={columns}
        rowGetter={this.state.data}
        rowsCount={this.state.data.length}
        minHeight={200}
        minWidth={200} />
    );
  }
}

export default ReactDataGridExample;

