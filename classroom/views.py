from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.authenticate import IsTeacherOrAdmin, IsAdmin
from classroom.models import *
from classroom.serializers import *
from member.models import Teacher
from .filters import CourseFilter, ScheduleFilter, TimeSlotFilter

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
        if self.request.user.groups.filter(name="admin").exists():
            return Course.objects.all()
        return Course.objects.filter(teacher__user=self.request.user)

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

class ScheduleViewset(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter

    # def list(self, request, *args, **kwargs):
    #     data = self.get_queryset().filter(weekday__in=request.data.get("weekdays", ""))
    #     return Response(ScheduleSerializer(data, many=True).data)

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def paginate_queryset(self, queryset):
        if self.request.query_params.get("pagination", False):
            return None
        return super().paginate_queryset(queryset)

class TimeSlotViewset(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    filterset_class = TimeSlotFilter

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [AllowAny]
        elif self.action in ['retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def paginate_queryset(self, queryset):
        if self.request.query_params.get("pagination", False):
            return None
        return super().paginate_queryset(queryset)


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
        if self.action in ['list']:
            permission_classes = [AllowAny]
        elif self.action in ['retrieve']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def paginate_queryset(self, queryset):
        if self.request.query_params.get("pagination", False):
            return None
        return super().paginate_queryset(queryset)

class SessionViewset(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="admin").exists():
            return Session.objects.all()
        return Session.objects.filter(course__teacher__user=self.request.user)

    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @transaction.atomic 
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        students = data.pop("students", [])
        serializer = SessionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()

        attendance = AttendanceSerializer(data=[{**student,"student": student["id"], "session": session.pk} for student in students], many=True)
        attendance.is_valid(raise_exception=True)
        attendance.save()

        return Response(serializer.data, status=201)

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

    def get_queryset(self):
        if self.request.user.groups.filter(name="admin").exists():
            return Attendance.objects.all()
        return Attendance.objects.filter(session__course__teacher__user=self.request.user)

    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
