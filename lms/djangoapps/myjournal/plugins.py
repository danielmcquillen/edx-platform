"""
Definition of the course myjournal feature.
"""
from django.utils.translation import ugettext_noop
from courseware.tabs import EnrolledTab
from . import is_feature_enabled


class MyJournalTab(EnrolledTab):
    """
    The representation of the course MyJournal view type.
    """

    name = "myjournal"
    title = "MyJournal"
    type = "myjournal"
    title = ugettext_noop("MyJournal")
    view_name = "myjournal_dashboard"
    is_default = "true"

    @classmethod
    def is_enabled(cls, course, user=None):
        """Returns true if the MyJournal feature is enabled in the course.

        Args:
            course (CourseDescriptor): the course using the feature
            user (User): the user interacting with the course
        """
        if not super(MyJournalTab, cls).is_enabled(course, user=user):
            return False

        return is_feature_enabled(course)
