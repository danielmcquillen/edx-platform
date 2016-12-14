/**
 * Model for a topic.
 */
(function(define) {
    'use strict';
    define(['backbone'], function(Backbone) {
        var Entry = Backbone.Model.extend({
            defaults: {
                id: '',
                name: '',
                description: '',
                team_count: 0,
                comments: []
            },

            initialize: function(options) {
                this.url = options.url;
            }
        });
        return Entry;
    });
}).call(this, define || RequireJS.define);
