"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import MyJournalDashboardView, EntryList, EntryDetail, CommentList

urlpatterns = patterns(
    'myjournal.views',
    url(r"^/$", login_required(MyJournalDashboardView.as_view()), name="myjournal_dashboard"),
    url(r'^/(?P<task_id>[0-9A-Za-z]+)/entries/$', login_required(EntryList.as_view()), name="myjournal_entry"),
    url(r'^/(?P<task_id>[0-9A-Za-z]+)/entries/(?P<entry_id>[0-9A-Za-z]+)/$', login_required(EntryDetail.as_view()), name="myjournal_entry"),
    url(r'^/(?P<task_id>[0-9A-Za-z]+)/entries/(?P<entry_id>[0-9A-Za-z]+)/comments/$', login_required(CommentList.as_view()), name="myjournal_comment"),
)
