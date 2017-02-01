"""Utility methods related to myjournal."""

from eventtracking import tracker
from track import contexts

def emit_myjournal_event(event_name, course_key, event_data):
    """
    Emit MyJournal events with the correct course id context.
    """
    context = contexts.course_context_from_course_id(course_key)

    with tracker.get_tracker().context(event_name, context):
        tracker.emit(event_name, event_data)
