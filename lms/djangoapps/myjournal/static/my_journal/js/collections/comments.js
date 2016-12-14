(function(define) {
    'use strict';
    define(['underscore', 'gettext', 'teams/js/models/comment'],
        function(_, gettext, CommentModel) {

            var CommentCollection = Backbone.Collection.extend({

                model: CommentModel,

                constructor: function(comments, options) {
                    if (comments.sort_order) {
                        this.state.sortKey = entries.sort_order;
                    }
                    options.perPage = entries.results.length;
                    BaseCollection.prototype.constructor.call(this, comments, options);

                    this.registerSortableField('updated', gettext('updated'));
                },

                onUpdate: function(event) {
                    if (_.contains(['create', 'delete'], event.action)) {
                        this.isStale = true;
                    }
                }
            });

            return TopicCollection;

        });
}).call(this, define || RequireJS.define);
