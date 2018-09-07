/*global TodoMVC:true, Backbone, $ */

var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var BackboneRadio = require('backbone.radio');
var App = require('./TodoMVC.Application');
var Layout = require('./TodoMVC.Layout');
var Todos = require('./TodoMVC.Todos');
var Views = require('./TodoMVC.TodoList.Views');
var Filter = require('./TodoMVC.FilterState');

'use strict';

var filterChannel = Backbone.Radio.channel('filter');

// TodoList Router
// ---------------
//
// Handles a single dynamic route to show
// the active vs complete todo items
module.exports.Router = Mn.AppRouter.extend({
    appRoutes: {
        '*filter': 'filterItems'
    }
});

// TodoList Controller (Mediator)
// ------------------------------
//
// Control the workflow and logic that exists at the application
// level, above the implementation detail of views and models
module.exports.Controller = Mn.Object.extend({

    initialize: function () {
        this.todoList = new Todos.TodoList();
    },

    // Start the app by showing the appropriate views
    // and fetching the list of todo items, if there are any
    start: function () {
        this.showHeader(this.todoList);
        this.showFooter(this.todoList);
        this.showTodoList(this.todoList);
        this.todoList.on('all', this.updateHiddenElements, this);
        this.todoList.fetch();
    },

    updateHiddenElements: function () {
        $('#main, #footer').toggle(!!this.todoList.length);
    },

    showHeader: function (todoList) {
        var header = new Layout.HeaderLayout({
            collection: todoList
        });
        App.root.showChildView('header', header);
    },

    showFooter: function (todoList) {
        var footer = new Layout.FooterLayout({
            collection: todoList
        });
        App.root.showChildView('footer', footer);
    },

    showTodoList: function (todoList) {
        App.root.showChildView('main', new Views.ListView({
            collection: todoList
        }));
    },

    // Set the filter to show complete or all items
    filterItems: function (filter) {
        var newFilter = filter && filter.trim() || 'all';
        filterChannel.request('filterState').set('filter', newFilter);
    }
});
