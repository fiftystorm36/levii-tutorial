/*global Backbone, TodoMVC:true */

var Backbone = require('backbone');
var Mn = require('backbone.marionette');
var Layout = require('./TodoMVC.Layout');

'use strict';

var TodoApp = Mn.Application.extend({
    setRootLayout: function () {
        this.root = new Layout.RootLayout();
    }
});

// The Application Object is responsible for kicking off
// a Marionette application when its start function is called
//
// This application has a singler root Layout that is attached
// before it is started.  Other system components can listen
// for the application start event, and perform initialization
// on that event

var TodoMVCApp = new TodoApp();

TodoMVCApp.on('before:start', function () {
    TodoMVCApp.setRootLayout();
});

module.exports = TodoMVCApp;
