"""
Defines common methods shared by Teams classes
"""

from django.conf import settings


def is_feature_enabled(course):
    """
    Returns True if the MyJournal feature is enabled.
    """
    return settings.FEATURES.get('ENABLE_MYJOURNAL', False) and course.myjournal_enabled
