
from opaque_keys.edx.keys import CourseKey
from courseware.courses import get_course_with_access, has_access
from student.models import CourseEnrollment
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_oauth.authentication import OAuth2Authentication
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import permissions
from rest_framework import generics
from lms.djangoapps.myjournal.models import CourseMyJournal, Task, Entry, Comment
from lms.djangoapps.myjournal.serializers import EntrySerializer, CommentSerializer, CommunityEntrySerializer
from . import is_feature_enabled

from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

DEFAULT_ENTRIES_PER_PAGE = 20



"""
    PERMISSIONS
    These permissions limit access to MyJournal endpoints
"""


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsMyJournalEnabled(permissions.BasePermission):
    """Permission that checks to see if this feature is enabled"""

    def has_object_permission(self, request, view, obj):
        course_key = CourseKey.from_string(request.course_id)
        course = get_course_with_access(request.user, "load", course_key)
        return is_feature_enabled(course)


class IsEnrolledOrIsStaff(permissions.BasePermission):
    """Permission that checks to see if the user is enrolled in the course or is staff."""

    def has_object_permission(self, request, view, obj):
        """Returns true if MyJournal is enabled and the user is enrolled. """

        course_key = CourseKey.from_string(request.course_id)
        course = get_course_with_access(request.user, "load", course_key)

        # Staff can see everything
        if bool(has_access(user, 'staff', course_key)):
            return true

        return CourseEnrollment.is_enrolled(request.user, course.id)




"""
    View classes
"""


class MyJournalDashboardView(GenericAPIView):
    """
        View methods related to the MyJournal dashboard.

        Renders the MyJournal dashboard, which is shown on the "MyJournal" tab.

        Raises a 404 if the course specified by course_id does not exist, the
        user is not registered for the course, or the MyJournal feature is not enabled.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "myjournal/myjournal.html"

    def get(self, request, course_id):

        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled(course):
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        is_staff = bool(has_access(user, 'staff', course_key))

        if not CourseEnrollment.is_enrolled(request.user, course.id) and not is_staff:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            myjournal = CourseMyJournal.objects.filter(course_id=course.id).first()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TODO : make this more elegant with serializer?
        tasks = []
        task_set = myjournal.tasks.all()
        for task in task_set:
            t = {'title': task.title,
                 'sequence': task.sequence,
                 'description': task.description,
                 'entry': {
                     'excerpt': task.entry.excerpt,
                     'url': reverse('entry_detail',
                                    kwargs={'course_id': str(course_id), 'task_id': str(task.id), 'entry_id': str(task.entry.id)},
                                    request=request),
                    },
                 'disable_courseware_js': True,
                 'uses_pattern_library': True,
                 }
            tasks.append(t)

        context = {
            "course": course,
            'csrf': csrf(request)['csrf_token'],
            "myjournal": myjournal,
            "tasks": tasks,
            "user_info": {
                "username": user.username,
                "staff": bool(has_access(user, 'staff', course_key)),
            },
            "myjournal_base_url": reverse('myjournal_dashboard', request=request, kwargs={'course_id': course_id}),
            "community_entries_url": reverse('community_entry_list', request=request, kwargs={'course_id': course_id}),
            "disable_courseware_js": True,
        }

        # TODO: Would rather use something django rest specific
        #       but can't use TemplateHTMLRenderer b/c we're using Mako templates...

        return Response(context)


class CommunityEntryList(GenericAPIView):
    """
      View entries from the entire community for this course.
    """

    # Do we need authentication_classes? The route already uses login_required in urls.py
    authentication_classes = (SessionAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated, IsMyJournalEnabled, IsEnrolledOrIsStaff, IsOwnerOrReadOnly)

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "myjournal/community_entry_list.html"

    def get(self, request, course_id, *args, **kwargs):
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        try:
            myjournal = CourseMyJournal.objects.filter(course_id=course.id).first()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        entries = Entry.objects.filter(myjournal_id=myjournal.id)
        serializer = CommunityEntrySerializer(entries, many=True)

        if format == "json" or format == "api":
            return Response(serializer.data)
        else:
            context = {
                "entries": serializer.data,
                "csrf": csrf(request)['csrf_token'],
                "course": course,
                "user_info": {
                    "username": request.user.username,
                    "staff": bool(has_access(request.user, 'staff', course_key)),
                },
                "myjournal_base_url": reverse('myjournal_dashboard', request=request, kwargs={'course_id': course_id}),
            }
            return Response(context)


class EntryDetail(generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated, IsMyJournalEnabled, IsEnrolledOrIsStaff, IsOwnerOrReadOnly)
    model = Entry
    serializer_class = EntrySerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "myjournal/entry.html"

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        serializer = EntrySerializer(entry)
        course_id = kwargs.get('course_id')
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)
        is_owner = entry.owner.id == request.user.id
        context = {
            "serializer": serializer,
            "entry": serializer.data,
            "task_title": entry.task.title,
            "task_description": entry.task.description,
            "course": course,
            'csrf': csrf(request)['csrf_token'],
            "user_info": {
                "username": request.user.username,
                "is_owner": is_owner,
                "staff": bool(has_access(request.user, 'staff', course_key)),
            },
            "entry_detail_url": reverse('entry_detail',
                                        request=request,
                                        kwargs={'course_id': course_id,
                                                'task_id': kwargs.get('task_id'),
                                                'entry_id': kwargs.get('entry_id')}),
            "myjournal_base_url": reverse('myjournal_dashboard',
                                          request=request,
                                          kwargs={'course_id': course_id}),
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        serializer = EntrySerializer(entry, data=request.data)
        course_id = kwargs.get('course_id')
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"})
        return Response({"status": status.HTTP_400_BAD_REQUEST})

    def delete(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        entry.delete()
        course_id = kwargs.get('course_id')
        redirect_url = reverse('myjournal_dashboard', request=request, kwargs={'course_id': course_id})
        return HttpResponseRedirect(redirect_url)


class CommunityEntryDetail(generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated, IsMyJournalEnabled, IsEnrolledOrIsStaff, IsOwnerOrReadOnly)
    model = Entry
    serializer_class = EntrySerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "myjournal/community_entry.html"

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        serializer = EntrySerializer(entry)
        course_id = kwargs.get('course_id')
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)
        is_owner = entry.owner.id == request.user.id
        context = {
            "serializer": serializer,
            "entry": serializer.data,
            "task_title": entry.task.title,
            "task_description": entry.task.description,
            "course": course,
            'csrf': csrf(request)['csrf_token'],
            "user_info": {
                "username": request.user.username,
                "is_owner": is_owner,
                "staff": bool(has_access(request.user, 'staff', course_key)),
            },
            "community_entry_detail_url": reverse('community_entry_detail',
                                                  request=request,
                                                  kwargs={'course_id': course_id,
                                                          'entry_id': kwargs.get('entry_id')}),
            "community_entry_comment_url": reverse('community_entry_comment',
                                                   request=request,
                                                   kwargs={'course_id': course_id,
                                                           'entry_id': kwargs.get('entry_id')}),
            "myjournal_base_url": reverse('myjournal_dashboard',
                                          request=request,
                                          kwargs={'course_id': course_id}),
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        serializer = EntrySerializer(entry, data=request.data)
        course_id = kwargs.get('course_id')
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"})
        return Response({"status": status.HTTP_400_BAD_REQUEST})

    def delete(self, request, *args, **kwargs):
        entry = self.get_object(kwargs.get('entry_id'))
        entry.delete()
        course_id = kwargs.get('course_id')
        redirect_url = reverse('myjournal_dashboard', request=request, kwargs={'course_id': course_id})
        return HttpResponseRedirect(redirect_url)


class CommentList(generics.GenericAPIView):

    # Do we need authentication_classes? The route already uses login_required in urls.py
    authentication_classes = (SessionAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAuthenticated, IsMyJournalEnabled, IsEnrolledOrIsStaff, IsOwnerOrReadOnly)

    renderer_classes = [JSONRenderer]

    def get(self, request, course_id, entry_id, *args, **kwargs):
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled(course):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        is_staff = bool(has_access(user, 'staff', course_key))

        if not CourseEnrollment.is_enrolled(request.user, course.id) and not is_staff:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Entry.objects.get(pk=entry_id, course_id=course.id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = entry.comments
        serializer = CommunityEntrySerializer(comments, many=True)

        return Response(serializer.data)

    def post(self, request, course_id, entry_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entry_id=entry_id, owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.GenericAPIView):

    authentication_classes = SessionAuthentication
    permission_classes = (permissions.IsAuthenticated, IsMyJournalEnabled, IsEnrolledOrIsStaff)

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        comment = self.get_object(kwargs.get('entry_id'))
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            redirect_url = reverse('myjournal_dashboard', request=request, kwargs={'course_id': course_id})
            return HttpResponseRedirect(redirect_url)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        entry_id = kwargs.get('entry_id')
        entry = self.get_object(entry_id)
        course_id = kwargs.get('course_id')
        entry.delete()
        redirect_url = reverse('entry_detail', request=request, kwargs={'course_id': course_id, 'entry_id': entry_id})
        return HttpResponseRedirect(redirect_url)

