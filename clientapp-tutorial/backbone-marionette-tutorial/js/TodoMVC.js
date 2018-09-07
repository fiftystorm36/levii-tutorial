/*global BackboneTodoMVC, TodoMVC:true, $ */

import "../node_modules/todomvc-app-css/index.css";
import "../node_modules/todomvc-common/base.css";
import "../css/app.css";

var Backbone = require('backbone');
var Mn = require('backbone.marionette');
var App = require('./TodoMVC.Application');
var Router = require('./TodoMVC.Router');

$(function () {
    'use strict';

    // After we initialize the app, we want to kick off the router
    // and controller, which will handle initializing our Views
    App.on('start', function () {
        var controller = new Router.Controller();
        controller.router = new Router.Router({
            controller: controller
        });

        controller.start();

        Backbone.history.start();
    });

    // start the TodoMVC app (defined in js/TodoMVC.js)
    App.start();
});
