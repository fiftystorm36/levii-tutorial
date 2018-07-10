webpackJsonp([1],{

/***/ 14:
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(1)(false);\n// imports\n\n\n// module\nexports.push([module.i, \".button {\\n  background: tomato;\\n  color: white; }\\n\", \"\"]);\n\n// exports\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/css-loader!./~/sass-loader/lib/loader.js!./src/Components/Button.scss\n// module id = 14\n// module chunks = 1\n\n//# sourceURL=webpack:///./src/Components/Button.scss?./~/css-loader!./~/sass-loader/lib/loader.js");

/***/ }),

/***/ 16:
/***/ (function(module, exports) {

eval("module.exports = \"<a class=\\\"button\\\" href=\\\"{{link}}\\\">{{text}}</a>\\n\";\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Button.html\n// module id = 16\n// module chunks = 1\n\n//# sourceURL=webpack:///./src/Components/Button.html?");

/***/ }),

/***/ 17:
/***/ (function(module, exports, __webpack_require__) {

eval("\nvar content = __webpack_require__(14);\n\nif(typeof content === 'string') content = [[module.i, content, '']];\n\nvar transform;\nvar insertInto;\n\n\n\nvar options = {\"hmr\":true}\n\noptions.transform = transform\noptions.insertInto = undefined;\n\nvar update = __webpack_require__(2)(content, options);\n\nif(content.locals) module.exports = content.locals;\n\nif(false) {\n\tmodule.hot.accept(\"!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Button.scss\", function() {\n\t\tvar newContent = require(\"!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Button.scss\");\n\n\t\tif(typeof newContent === 'string') newContent = [[module.id, newContent, '']];\n\n\t\tvar locals = (function(a, b) {\n\t\t\tvar key, idx = 0;\n\n\t\t\tfor(key in a) {\n\t\t\t\tif(!b || a[key] !== b[key]) return false;\n\t\t\t\tidx++;\n\t\t\t}\n\n\t\t\tfor(key in b) idx--;\n\n\t\t\treturn idx === 0;\n\t\t}(content.locals, newContent.locals));\n\n\t\tif(!locals) throw new Error('Aborting CSS HMR due to changed css-modules locals.');\n\n\t\tupdate(newContent);\n\t});\n\n\tmodule.hot.dispose(function() { update(); });\n}\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Button.scss\n// module id = 17\n// module chunks = 1\n\n//# sourceURL=webpack:///./src/Components/Button.scss?");

/***/ }),

/***/ 3:
/***/ (function(module, exports, __webpack_require__) {

eval("\n/* injects from baggage-loader */\nvar template = __webpack_require__(16);\n__webpack_require__(17);\n\n'use strict';\n\nObject.defineProperty(exports, \"__esModule\", {\n    value: true\n});\n\nvar _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if (\"value\" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }(); // src/Components/Button.js\n\n\nvar _jquery = __webpack_require__(10);\n\nvar _jquery2 = _interopRequireDefault(_jquery);\n\nvar _mustache = __webpack_require__(11);\n\nvar _mustache2 = _interopRequireDefault(_mustache);\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar Button = function () {\n    function Button(link) {\n        _classCallCheck(this, Button);\n\n        this.link = link;\n    }\n\n    _createClass(Button, [{\n        key: 'onClick',\n        value: function onClick(event) {\n            event.preventDefault();\n            alert(this.link);\n        }\n    }, {\n        key: 'render',\n        value: function render(node) {\n            var text = (0, _jquery2.default)(node).text();\n            // ボタンの描画\n            (0, _jquery2.default)(node).html(_mustache2.default.render(template, { text: text }));\n            // リスナーを割り当て\n            (0, _jquery2.default)('.button').click(this.onClick.bind(this));\n        }\n    }]);\n\n    return Button;\n}();\n\nexports.default = Button;\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Button.js\n// module id = 3\n// module chunks = 1\n\n//# sourceURL=webpack:///./src/Components/Button.js?");

/***/ })

});