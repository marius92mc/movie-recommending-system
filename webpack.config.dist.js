'use strict';

var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: {
    reactApp: ['./app/templates/client/index.js']
  },

  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel?stage=0&loose=all', exclude: /node_modules/ },
      { test: /\.scss$/, loader: 'css?modules&localIdentName=[local]!postcss!sass'},
      {
         test: /\.(jpe?g|png|gif|svg)$/i,
         loaders: [
           'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]'
         ]
      }
    ]
  },

  externals: {
    'react': 'react',
    'react-dom': 'ReactDOM',
  },

  output: {
    filename: './app/static/bundle.js',
    libraryTarget: 'umd',
    library: 'FacebookLogin'
  },

  resolve: {
    extensions: ['', '.js']
  },

  plugins: [
    new webpack.optimize.DedupePlugin()
  ]
};
