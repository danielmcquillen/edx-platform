"""
Admin registration for MyJournal
"""
from django.contrib import admin
from lms.djangoapps.myjournal.models import CourseMyJournal, Task, Entry, Comment
# from config_models.admin import ConfigurationModelAdmin

admin.site.register(CourseMyJournal)
admin.site.register(Task)
admin.site.register(Entry)
admin.site.register(Comment)

# Example from badges of registering a model for configuration (based on ConfigurationModel)
# Use the standard Configuration Model Admin handler for this model.
# admin.site.register(CourseEventBadgesConfiguration, ConfigurationModelAdmin)
