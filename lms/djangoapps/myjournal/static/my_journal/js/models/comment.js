/**
 * Model for a topic.
 */
(function(define) {
    'use strict';
    define(['backbone'], function(Backbone) {
        var Comment = Backbone.Model.extend({
            defaults: {
                id: '',
                text: '',
								flag: false,
								user_name: '',
								user_profile_url: '',
								updated: ''
            },

            initialize: function(options) {
                this.url = options.url;
            }
        });
        return Entry;
    });
}).call(this, define || RequireJS.define);
