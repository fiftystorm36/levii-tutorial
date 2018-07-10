var webpack = require('webpack');
var CleanPlugin = require('clean-webpack-plugin');
//var ExtractPlugin = require('extract-text-webpack-plugin');
var production = process.env.NODE_ENV === 'production';


var plugins = [
    //new ExtractPlugin('bundle.css', {allChunks: true}),
    new webpack.optimize.CommonsChunkPlugin({
        name:      'main', // 依存性を主(main)ファイルに移す
        children:  true,   // 全ての子に対しても共通する依存性を探す
        minChunks: 2,      // この回数、依存性に遭遇したら抜き出す
    }),

];

if (production) {
    plugins = plugins.concat([
        // このプラグインは同名のチャンクとファイルを探し、
        // キャッシュ向上のために、これらをマージします
        new webpack.optimize.DedupePlugin(),
        // このプラグインは、チャンクとモジュールが
        // アプリケーション内でどれだけ使用されているかによって
        // 最適化を行います。
        //new webpack.optimize.OccurenceOrderPlugin(),
        // このプラグインはWebpackに作成されるチャンクのサイズが小さくなりすぎることで、
        // 読み込み効率が悪くなることを防ぎます。
        new webpack.optimize.MinChunkSizePlugin({
            minChunkSize: 51200, // ~50kb
        }),
        // このプラグインは最終的なバンドルの全てのJavaScriptコードを
        // 圧縮(minify)します。
        new webpack.optimize.UglifyJsPlugin({
            mangle:   true,
            compress: {
                warnings: false, // uglificationの警告を隠します
            },
        }),
        // このプラグインは、製品版でfalseを設定することができる様々な変数を定義し、
        // 最終的なバンドルでのコンパイルから、それらに関連するコードを避けるためことができます。
        new webpack.DefinePlugin({
            __SERVER__:      !production,
            __DEVELOPMENT__: !production,
            __DEVTOOLS__:    !production,
            'process.env':   {
                BABEL_ENV: JSON.stringify(process.env.NODE_ENV),
            },
        }),

        new webpack.LoaderOptionsPlugin({
            debug: true
        }),

        new CleanPlugin('builds'),
    ]);
}

module.exports = {
    entry: __dirname + '/src',
    output: {
        path: __dirname +'/builds',
        filename: production ? '[name]-[hash].js' : 'bundle.js',
        chunkFilename: '[name]-[chunkhash].js',
        publicPath: 'builds/',
    },
    devServer: {
        contentBase: __dirname,
    },

    plugins: plugins,

    module: {
        rules: [
            {
                test: /\.js/,
                loader: 'eslint-loader',
                enforce: 'pre',
            },
            {
                test: /\.js/,
                loader: 'baggage-loader?[file].html=template&[file].scss',
            },
            {
                test:   /\.js$/,
                use: 'babel-loader',
                include: __dirname + '/src',
            },
            {
                test:   /\.scss/,
                use:
                    [
                        'style-loader',
                        'css-loader',
                        'sass-loader'],
            },
            {
                test:   /\.html/,
                use: 'html-loader',
            },
            {
                test: /\.(jpe?g|png)$/,
                use: {
                    loader: "url-loader",
                    options: {
                        limit: 1000,
                    },
                },
            }
        ],
    },
    devtool: production ? false : 'eval',
};
