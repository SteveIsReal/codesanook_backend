from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account.authenticate import IsTeacherOrAdmin, IsAdmin
from classroom.models import *
from classroom.serializers import *
from member.models import Teacher
from .filters import CourseFilter

class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

class CouseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

    def get_queryset(self):
        if self.request.user.groups.filter(name="admin"):
            return Course.objects.all()
        return Course.objects.filter(teacher=Teacher.objects.filter(user=self.request.user).first())

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'sessions', 'curriculum', 'time_slots']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        course = self.get_object()
        queryset = course.sessions.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SessionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SessionSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def curriculum(self, request, pk=None):
        course = self.get_object()
        serializer = CurriculumSerializer(course.curriculum)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def time_slots(self, request, pk=None):
        course = self.get_object()
        serializer = TimeSlotSerializer(course.time_slots.all(), many=True)

        return Response(serializer.data)

class TimeSlotViewset(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class SubjectViewset(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

class CurriculumViewset(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

class SessionViewset(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsTeacherOrAdmin]

    def create(self, request, *args, **kwargs):
        students = request.data.pop("students", [])
        serializer = SessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        for student in students:
            student['student'] = student['id']
            attendance = AttendanceSerializer(data={**student, "session": session.pk})
            attendance.is_valid(raise_exception=True)
            attendance.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        students = request.data.pop("students", [])
        instance = self.get_object()
        serializer = SessionSerializer(instance, data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        session = serializer.save()

        for student in students:
            attendance_instance = Attendance.objects.filter(student=student["id"], session=session).first()
            attendance = AttendanceSerializer(attendance_instance, data={**student, "student": student["id"], "session": session.pk}, partial=True)
            attendance.is_valid(raise_exception=True)
            attendance.save()

        return Response(serializer.data)

class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrAdmin]
