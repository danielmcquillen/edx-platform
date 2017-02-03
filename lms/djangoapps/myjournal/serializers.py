from rest_framework import serializers
from lms.djangoapps.myjournal.models import Task, Entry, Comment
from openedx.core.djangoapps.user_api.accounts.image_helpers import get_profile_image_urls_for_user


class OwnerListingField(serializers.RelatedField):
    """
    A serializer to provide user information when shown as owner
    next to entry or comment in community entries.
    """

    def to_representation(self, value):
        pimage_url = get_profile_image_urls_for_user(value)
        return {"id": value.id,
                "profile_image_url": pimage_url['small'],
                "username": value.username}


class EntryListingField(serializers.RelatedField):
    """
    A serializer to just show limited amount of entry information
    when showing an entry as a child object of task.
    """
    def to_representation(self, value):
        return {"id": value.id, "excerpt": value.excerpt}


class CommentSerializer(serializers.ModelSerializer):

    owner = OwnerListingField(many=False, read_only=True)
    entry = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'entry', 'text', 'flag', 'owner')
        read_only_fields = ('id', 'entry', 'owner', 'flag')


class EntrySerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'myjournal', 'task', 'owner', 'comments', 'text', 'excerpt', 'is_private')
        read_only_fields = ('id', 'myjournal', 'task', 'owner', 'comments')

    def get_owner_entry(self, obj):
        owner = self.context['request'].user
        zone_permission = Entry.objects.get(task=obj, owner=owner)
        serializer = EntrySerializer(zone_permission)
        return serializer.data


class CommunityEntrySerializer(serializers.ModelSerializer):
    """ This serializer includes name of related task"""

    comments = CommentSerializer(many=True, read_only=True)
    task = serializers.StringRelatedField(many=False)
    owner = OwnerListingField(many=False, read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'myjournal', 'task', 'excerpt', 'owner', 'is_private', 'comments')
        read_only_fields = ('id', 'myjournal', 'task', 'excerpt', 'owner', 'is_private', 'comments')


class TaskSerializer(serializers.ModelSerializer):
    """ Don't include full entry here using a serializer, as each entry has
        a lot of text and comments and that's a lot to send down the wire.
        Instead use a custom serializer that just shows entry id and excerpt."""
    entries = EntryListingField(source='entries', many=False, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'owner', 'description', 'sequence')



