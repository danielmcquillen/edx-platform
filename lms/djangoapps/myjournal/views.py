
from opaque_keys.edx.keys import CourseKey
from courseware.courses import get_course_with_access, has_access
from student.models import CourseEnrollment, CourseAccessRole
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, filters, status
from rest_framework.response import Response
from lms.djangoapps.myjournal.models import CourseMyJournal, Task, Entry, Comment
from lms.djangoapps.myjournal.serializers import EntrySerializer, CommentSerializer
from . import is_feature_enabled

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist


class MyJournalDashboardView(GenericAPIView):

    def get(self, request, course_id):
        """
        View methods related to the MyJournal dashboard.

        Renders the MyJournal dashboard, which is shown on the "MyJournal" tab.

        Raises a 404 if the course specified by course_id does not exist, the
        user is not registered for the course, or the MyJournal feature is not enabled.
        """

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

        mj_tasks = myjournal.task_set.all()

        context = {
            "course": course,
            "course_id": course_key,
            'csrf': csrf(request)['csrf_token'],
            "myjournal": myjournal,
            "tasks": mj_tasks,
            "user_info": {
                "username": user.username,
                "staff": bool(has_access(user, 'staff', course_key)),
            },
            "disable_courseware_js": True,
        }
        return render_to_response("myjournal/myjournal.html", context)


class EntryList(GenericAPIView):
    """
    A list of entries for a given MyJournal task in a course.
    """
    def get(self, request, course_id, task_id, **kwargs):

        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled(course):
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        is_staff = bool(has_access(user, 'staff', course_key))

        if CourseEnrollment.is_enrolled(request.user, course.id) and not is_staff:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # We want the task information *and* the user's entry, if any.
        try:
            mj_task = Task.objects.get(pk=task_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        entries = mj_task.entry_set.filter(private=False)

        context = {
            'csrf': csrf(request)['csrf_token'],
            "course_id": course_key,
            "course": course,
            "task": mj_task,
            "entries": entries,
            "user_info": {
                "username": user.username,
                "is_staff": bool(is_staff),
            },
            "disable_courseware_js": True,
        }

        return render_to_response("myjournal/entry_list.html", context)

    def post(self, request, format=None):

        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntryDetail(GenericAPIView):

    def get(self, request, course_id, task_id, entry_id,  **kwargs):

        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled(course):
            raise Http404

        user = request.user
        is_staff = bool(has_access(user, 'staff', course_key))

        # We want the task information *and* the user's entry, if any.
        try:
            mj_task = Task.objects.get(pk=task_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            mj_entry = Entry.objects.get(pk=entry_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        is_own_entry = mj_entry.user == user
        is_private = mj_entry.private

        if not is_own_entry and is_private:
            return Response(status=status.HTTP_404_NOT_FOUND)

        entry_comments = mj_entry.entry_comment_set.filter(hide=False)

        context = {
            'csrf': csrf(request)['csrf_token'],
            "course_id": course_key,
            "course": course,
            "task": mj_task,
            "entry": mj_entry,
            "comments": entry_comments,
            "is_own_entry": is_own_entry,
            "is_private": is_private,
            "disable_courseware_js": True,
            "user_info": {
                "username": user.username,
                "staff": bool(is_staff),
            },
            "comments": entry_comments
        }

        if is_own_entry:
            context["entry"] = mj_entry
            context["entry_form"] = entry_form
            context["entry_form_updated"] = entry_form_updated
        else:
            context["entry_comment_form"] = entry_comment_form

        return render_to_response("myjournal/entry.html", context)

    def post(self, request, format=None):
        # TODO
        pass


class CommentList(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
        Views related to comments by students on an entry.
    """

    def get(self, request, course_id, task_id, entry_id, comment_id=None):

        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        if not is_feature_enabled(course):
            raise Http404

        if not CourseEnrollment.is_enrolled(request.user, course.id) and \
                not has_access(request.user, 'staff', course, course.id):
            raise Http404

        user = request.user

        try:
            mj_entry = Entry.objects.get(pk=entry_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        is_own_entry = mj_entry.user == user
        is_private = mj_entry.private

        if not is_own_entry and is_private:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = mj_entry.entry_comment_set.filter(hide=False)
        serializer = EntrySerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, course_id, task_id, entry_id,):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
