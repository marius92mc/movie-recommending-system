'use strict';

var path = require('path');
var webpack = require('webpack');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

// Where are your assets located in your project? This would typically be a path
// that contains folders such as: images, stylesheets and javascript.
var rootAssetPath = './app/client_assets';

module.exports = {
  entry: {
    reactApp: ['./app/templates/client/index.js']
  },

  module: {
    loaders: [
      {
        test: /\.js$/, loader: 'babel?stage=0&loose=all', exclude: /node_modules/
      },
      {
        test: /\.scss$/, loader: 'css?modules&localIdentName=[local]!postcss!sass'
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        loaders: [
            'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]'
        ]
      }
    ]
  },

  output: {
    filename: './app/static/bundle.js'
  },

  resolve: {
    extensions: ['', '.js']
  },

  plugins: [
      new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
        rootAssetPath: rootAssetPath,
        ignorePaths: ['/stylesheets', '/javascript']
      }),
      new webpack.HotModuleReplacementPlugin()
  ],

  devServer: {
    contentBase: './app/templates/client'
  }
};
/*
'use strict';

var path = require('path');
var webpack = require('webpack');

module.exports = {

  devtool: 'eval',

  entry: {
    demo: ['webpack/hot/dev-server', './demo/index.js']
  },

  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel?stage=0', exclude: /node_modules/ },
      { test: /\.scss$/, loader: 'css?modules&localIdentName=[local]!postcss!sass'}
    ]
  },

  output: {
    filename: 'demo/bundle.js'
  },

  resolve: {
    extensions: ['', '.js'],
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],

  devServer: {
    contentBase: './demo'
  }
};
*/
