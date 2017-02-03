"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import MyJournalDashboardView, CommunityEntryList, CommunityEntryDetail, EntryDetail, CommentList


urlpatterns = patterns(
    'myjournal.views',
    url(r"^/$",
        login_required(MyJournalDashboardView.as_view()),
        name="myjournal_dashboard"),

    # COMMUNITY VIEWS

    url(r"^/community/entries/$",
        login_required(CommunityEntryList.as_view()),
        name="community_entry_list"),

    # This should probably point to diff view? For expediency's sake using same view as owner view.
    # TODO refactor
    url(r"^/community/entries/(?P<entry_id>[0-9A-Za-z]+)/$",
        login_required(CommunityEntryDetail.as_view()),
        name="community_entry_detail"),

    url(r"^/community/entries/(?P<entry_id>[0-9A-Za-z]+)/comments$",
        login_required(CommentList.as_view()),
        name="community_entry_comment"),

    # OWNER VIEWS

    url(r"^/tasks/(?P<task_id>[0-9A-Za-z]+)/entries/(?P<entry_id>[0-9A-Za-z]+)/$",
        login_required(EntryDetail.as_view()),
        name="entry_detail"),

)
