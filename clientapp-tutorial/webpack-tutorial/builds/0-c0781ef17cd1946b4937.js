webpackJsonp([0],{

/***/ 12:
/***/ (function(module, exports) {

eval("module.exports = \"<header class=\\\"header\\\">{{text}}</header>\\n\";\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Header.html\n// module id = 12\n// module chunks = 0\n\n//# sourceURL=webpack:///./src/Components/Header.html?");

/***/ }),

/***/ 13:
/***/ (function(module, exports, __webpack_require__) {

eval("\nvar content = __webpack_require__(15);\n\nif(typeof content === 'string') content = [[module.i, content, '']];\n\nvar transform;\nvar insertInto;\n\n\n\nvar options = {\"hmr\":true}\n\noptions.transform = transform\noptions.insertInto = undefined;\n\nvar update = __webpack_require__(2)(content, options);\n\nif(content.locals) module.exports = content.locals;\n\nif(false) {\n\tmodule.hot.accept(\"!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Header.scss\", function() {\n\t\tvar newContent = require(\"!!../../node_modules/css-loader/index.js!../../node_modules/sass-loader/lib/loader.js!./Header.scss\");\n\n\t\tif(typeof newContent === 'string') newContent = [[module.id, newContent, '']];\n\n\t\tvar locals = (function(a, b) {\n\t\t\tvar key, idx = 0;\n\n\t\t\tfor(key in a) {\n\t\t\t\tif(!b || a[key] !== b[key]) return false;\n\t\t\t\tidx++;\n\t\t\t}\n\n\t\t\tfor(key in b) idx--;\n\n\t\t\treturn idx === 0;\n\t\t}(content.locals, newContent.locals));\n\n\t\tif(!locals) throw new Error('Aborting CSS HMR due to changed css-modules locals.');\n\n\t\tupdate(newContent);\n\t});\n\n\tmodule.hot.dispose(function() { update(); });\n}\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Header.scss\n// module id = 13\n// module chunks = 0\n\n//# sourceURL=webpack:///./src/Components/Header.scss?");

/***/ }),

/***/ 15:
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(1)(false);\n// imports\n\n\n// module\nexports.push([module.i, \".header {\\n  font-size: 3rem; }\\n\", \"\"]);\n\n// exports\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/css-loader!./~/sass-loader/lib/loader.js!./src/Components/Header.scss\n// module id = 15\n// module chunks = 0\n\n//# sourceURL=webpack:///./src/Components/Header.scss?./~/css-loader!./~/sass-loader/lib/loader.js");

/***/ }),

/***/ 4:
/***/ (function(module, exports, __webpack_require__) {

eval("\n/* injects from baggage-loader */\nvar template = __webpack_require__(12);\n__webpack_require__(13);\n\n'use strict';\n\nObject.defineProperty(exports, \"__esModule\", {\n    value: true\n});\n\nvar _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if (\"value\" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();\n\nvar _jquery = __webpack_require__(10);\n\nvar _jquery2 = _interopRequireDefault(_jquery);\n\nvar _mustache = __webpack_require__(11);\n\nvar _mustache2 = _interopRequireDefault(_mustache);\n\nvar _Header = __webpack_require__(12);\n\nvar _Header2 = _interopRequireDefault(_Header);\n\n__webpack_require__(13);\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar Header = function () {\n    function Header() {\n        _classCallCheck(this, Header);\n    }\n\n    _createClass(Header, [{\n        key: 'render',\n        value: function render(node) {\n            var text = (0, _jquery2.default)(node).text();\n            (0, _jquery2.default)(node).html(_mustache2.default.render(_Header2.default, { text: text }));\n        }\n    }]);\n\n    return Header;\n}();\n\nexports.default = Header;\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/Components/Header.js\n// module id = 4\n// module chunks = 0\n\n//# sourceURL=webpack:///./src/Components/Header.js?");

/***/ })

});