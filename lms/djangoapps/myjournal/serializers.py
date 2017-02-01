from rest_framework import serializers
from lms.djangoapps.myjournal.models import CourseMyJournal, Task, Entry, Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('id', 'text', 'flag')


class EntrySerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'comments')

