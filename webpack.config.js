// webpack configuration file

const webpack = require('webpack');
const path = require('path');

module.exports = {
    entry: ["./src/entry.ts"],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: "bundle.js"
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.ts$/,
                loader: 'ts-loader',
                options: {
                    appendTsSuffixTo: [/\.vue$/]
                }
            },
            // BEGIN rules needed for element-ui
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader', 'postcss-loader']
            },
            {
                test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                    }
                }]
            }
            // END rules needed for element-ui
        ],
        loaders: [
        ]
    },
    devtool: 'inline-source-map',
    devServer: {
        port: 57238,
        proxy: {
            "/api": {
                target: "http://localhost:5000",
                pathRewrite: {"^/api": ""}
            }
        }
    }
};
