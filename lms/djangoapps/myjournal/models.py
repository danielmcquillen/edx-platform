""" Django models related to MyJournal functionality"""

from django.db import models
from django.contrib.auth.models import User
from xmodule_django.models import CourseKeyField
from uuid import uuid4
from util.model_utils import slugify

# States that a MyJournal Entry can be in.
MYJOURAL_ENTRY_PRIVATE = 0
MYJOURAL_ENTRY_PUBLIC = 1

# States that a Entry Comment can be in
COMMENT_FLAG_OK=0
COMMENT_FLAG_INAPPROPRIATE=1

class CourseMyJournal(models.Model):
    """
    Describes a MyJournal instance attached to a course.
    """
    myjournal_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    # Accoding to notes in problem-building, should use course_key, not course_id
    course_id = CourseKeyField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "myjournal"

    @classmethod
    def create(cls, title, course_id, description):
        """Create a complete MyJournal object for a course.

        Args:
            title (str): The title of the MyJournal to be created.
            course_id (str): The ID string of the course associated
              with this team.
            description (str): A description of MyJournal instance, e.g. it's
              purpose within the course.

        """
        unique_id = uuid4().hex
        myjournal_id = slugify(title)[0:20] + '-' + unique_id

        course_myjournal = cls(
            myjournal_id=myjournal_id,
            title=title,
            course_id=course_id,
            description=description
        )

        return course_myjournal

    def __repr__(self):
        return "<MyJournal myjournal_id={0.myjournal_id}>".format(self)


class Task(models.Model):
    """
    Describes a specific entry task in a course's MyJournal.
    This task appears in their MyJournal page as a blank entry
    with some instructions about what they should write.
    """
    myjournal = models.ForeignKey(CourseMyJournal, db_index=True)
    sequence = models.IntegerField('Where this entry is positioning in MyJournal list of entries for course.')
    title = models.CharField('Title for entry', max_length=255)
    description = models.TextField('Instructor description of entry task')

    class Meta:
        app_label = "myjournal"
        ordering = ['sequence', ]


class Entry(models.Model):
    """
    Entry model class providing the fields and methods required for publishing
    a student's submissions for an entry in a MyJournal course instance,
    over time and with the ability to modifying the entry's visibility.
    """

    STATUS_CHOICES = ((MYJOURAL_ENTRY_PRIVATE, 'private'),
                      (MYJOURAL_ENTRY_PUBLIC, 'public'))
    task = models.ForeignKey(Task, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    private = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, help_text="Used to build the entry's URL.")
    status = models.IntegerField(db_index=True, choices=STATUS_CHOICES, default=MYJOURAL_ENTRY_PRIVATE)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)

    class Meta(object):
        app_label = "myjournal"

    @classmethod
    def create(cls, task, user):
        """Create a blank Entry object for a MyJournal task.

        Args:
            task (str):     The Task this Entry is related to.
            user (object):  The user object for the student making this entry.

        """

        entry = cls(
            task=task,
            user=user,
            title="",
            text=""
        )

        return entry


class Comment(models.Model):
    """
    A comment on a student's MyJounal Entry.
    Can be made on an Entry by the author or another student.
    """
    FLAG_CHOICES = ((COMMENT_FLAG_OK, 'OK'),
                      (COMMENT_FLAG_INAPPROPRIATE, 'Flagged as inappropriate'))
    entry = models.ForeignKey(Entry, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    text = models.TextField(blank=True)
    flag = models.IntegerField(db_index=True, choices=FLAG_CHOICES, default=COMMENT_FLAG_OK)
    #Hide function allows admin to hide comment if truly inappropriate
    hide = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)

    class Meta(object):
        app_label = "myjournal"