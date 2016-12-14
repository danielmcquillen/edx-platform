(function(define) {
    'use strict';
    define(['underscore', 'gettext', 'teams/js/models/entry'],
        function(_, gettext, EntryModel) {

            var EntryCollection = Backbone.Collection.extend({

                model: EntryModel,

                state: {
                    sortKey: 'updated'
                },

                constructor: function(entries, options) {
                    if (entries.sort_order) {
                        this.state.sortKey = entries.sort_order;
                    }
                    options.perPage = entries.results.length;
                    BaseCollection.prototype.constructor.call(this, entries, options);

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
