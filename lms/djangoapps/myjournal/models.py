""" Django models related to MyJournal functionality"""

from django.db import models
from django.contrib.auth.models import User
from xmodule_django.models import CourseKeyField
from uuid import uuid4
from util.model_utils import slugify

# States that a MyJournal Entry can be in.
MYJOURNAL_ENTRY_PRIVATE = 0
MYJOURNAL_ENTRY_PUBLIC = 1

# States that a Entry Comment can be in
COMMENT_FLAG_OK = 0
COMMENT_FLAG_INAPPROPRIATE = 1


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
    myjournal = models.ForeignKey(CourseMyJournal, related_name="tasks", db_index=True)
    sequence = models.IntegerField('Where this entry is positioned in MyJournal list of entries for course.')
    title = models.CharField('Title for entry', max_length=255)
    description = models.TextField('Instructor description of entry task')

    class Meta:
        app_label = "myjournal"
        ordering = ['sequence', ]

    def __unicode__(self):
        return "%d: %s" % (self.sequence, self.title)


class Entry(models.Model):
    """
    Entry model class providing the fields and methods required for publishing
    a student's submissions for an entry in a MyJournal course instance,
    over time and with the ability to modifying the entry's visibility.

    A foreign key to myjournal is included, rather than relying on relation through Task.
    This allows a quicker lookup of entries by course.
    """

    myjournal = models.ForeignKey(CourseMyJournal, db_index=True, related_name='entries', on_delete=models.CASCADE)
    task = models.OneToOneField(Task, related_name="entry",  on_delete=models.CASCADE)
    owner = models.ForeignKey(User, db_index=True)
    text = models.TextField(blank=True, max_length=20000)
    excerpt = models.TextField(blank=True, editable=False)
    is_private = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta(object):
        app_label = "myjournal"
        ordering = ['updated', ]

    @classmethod
    def create(cls, myjournal, task, user):
        """Create a blank Entry object for a MyJournal task.

        Args:
            task (str):     The Task this Entry is related to.
            user (object):  The user object for the student making this entry.

        """

        entry = cls(
            myjournal=myjournal,
            task=task,
            user=user,
            title="",
            text=""
        )

        return entry

    def save(self, *args, **kwargs):
        """
            Create an excerpt from entry text before finishing save.
        """
        self.excerpt = (self.text[:75] + '...') if len(self.text) > 75 else self.text
        super(Entry, self).save(*args, **kwargs)  # Call the "real" save() method.


class Comment(models.Model):
    """
    A comment on a specific MyJournal Entry.
    Can be made on an Entry by the author or another student.
    """
    FLAG_CHOICES = ((COMMENT_FLAG_OK, 'OK'),
                      (COMMENT_FLAG_INAPPROPRIATE, 'Flagged as inappropriate'))
    entry = models.ForeignKey(Entry, db_index=True, related_name="comments", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, db_index=True)
    text = models.TextField(blank=True, max_length=5000)
    flag = models.IntegerField(db_index=True, choices=FLAG_CHOICES, default=COMMENT_FLAG_OK)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    # Hide property allows admin to hide comment if truly inappropriate
    hide = models.BooleanField(default=False)

    class Meta(object):
        app_label = "myjournal"
        ordering = ['updated', ]
