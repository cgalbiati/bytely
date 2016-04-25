var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: [
    'babel-polyfill',
    'webpack-dev-server/client?http://localhost:8080',
    'webpack/hot/only-dev-server',
    './src/main'
  ],
  output: {
      path: path.resolve(__dirname, "public/build"),
      publicPath: '/static/',
      filename: 'bundle.js'
  },
  devtool: 'source-map',
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  module: {
    loaders: [
      // transpile all js files from ES6 to ES5
      {
        test: /\.js$/,
        include: path.join(__dirname, 'src/react'),
        loaders: ['react-hot', 'babel-loader?presets[]=es2015'],
        // exclude: /node_modules/
      }, 

      //jsx, es6
      {
        test: /\.jsx$/,
        include: path.join(__dirname, 'src/react'),
        loaders: ['react-hot', 'babel-loader?presets[]=react,presets[]=es2015'],
        // exclude: /node_modules/
      }
    ]
  },
  devServer: {
    //this serves the index.html from the djengo app, but means it can't find the css file
    contentBase: "../templates"
  },
  debug: true
};



function getEntrySources(sources) {
    if (process.env.NODE_ENV !== 'production') {
        sources.push('webpack-dev-server/client?http://localhost:8080');
        sources.push('webpack/hot/only-dev-server');
    }

    return sources;
}