/**
 * Model for a team.
 */
(function(define) {
    'use strict';
    define(['backbone'], function(Backbone) {
        var MyJournal = Backbone.Model.extend({
            defaults: {
                id: null,
                title: '',
                description: '',
                course_id: '',
                topic_id: '',
                tasks: []
            },

            initialize: function(options) {
                this.url = options.url;
            }
        });
        return MyJournal;
    });
}).call(this, define || RequireJS.define);
