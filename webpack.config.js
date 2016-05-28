var path = require('path');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

// Where are your assets located in your project? This would typically be a path
// that contains folders such as: images, stylesheets and javascript.
var rootAssetPath = './app/client';

module.exports = {
  module: {
    loaders: [
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        loaders: [
            'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]'
        ]
      }
    ]
  },
  plugins: [
    new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
        rootAssetPath: rootAssetPath,
        ignorePaths: ['/stylesheets', '/javascript']
    })
  ]
};