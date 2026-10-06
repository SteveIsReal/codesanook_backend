from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from classroom.models import *
from classroom.serializers import *

class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CouseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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

class SubjectViewset(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CurriculumViewset(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

class SessionViewset(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

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