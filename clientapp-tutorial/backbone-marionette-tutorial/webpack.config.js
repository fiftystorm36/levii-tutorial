const path = require('path');
const webpack = require('webpack');

const config = {
    entry: './js/TodoMVC.js',
    output: {
        path: __dirname + '/build',
        filename: 'bundle.js',
    },
    module: {
        loaders: [
            {
                test: /\.css$/,
                loader: ['style-loader','css-loader']
            },
            {
                test: /\.hbs$/,
                loader: ['handlebars-loader']
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin(
            {
                jQuery: "jquery",
                $: "jquery",
                _: "underscore",
            }
        )
    ]
};

module.exports = config;
