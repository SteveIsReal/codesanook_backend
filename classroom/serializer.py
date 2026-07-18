from rest_framework import serializers
from classroom.models import *

class CourseSerializer(serializers.ModelSerializer):

    teacher = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    used_session_count = serializers.IntegerField()

    def get_teacher(self, obj):
        return obj.teacher.user.first_name

    def get_students(self, obj):
        return [i.name for i in obj.students.all()]

    class Meta:
        model = Course
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"