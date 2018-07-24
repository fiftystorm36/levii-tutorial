const WebpackNotifierPlugin = require('webpack-notifier');
const path = require('path');

module.exports = {
    mode: 'development',
    devtool: 'inline-source-map',
    entry: path.resolve(__dirname, 'src/index.js'),
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: "bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015'],
                    plugins: ['babel-plugin-espower', 'espower']
                }
            }
        ]
    },
    resolve: {
        extensions: ['.js']
    },
    plugins: [
        new WebpackNotifierPlugin({title: 'Webpack'})
    ]
};
