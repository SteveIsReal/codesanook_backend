from rest_framework import serializers
from classroom.models import *


class TimeSlotSerializer(serializers.ModelSerializer):

    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_name = serializers.CharField()

    def validate(self, attrs):
        avaliable_qs = TimeSlot.objects.check_avaliable(
            start_time=attrs['start_time'],
            end_time=attrs['end_time'],
            weekday=attrs['weekday'],
            room=attrs['room']
        )

        if self.instance:
            avaliable_qs = avaliable_qs.exclude(id=self.instance.id)

        if avaliable_qs.exist():
            return serializers.ValidationError({"info": "nah"})

        return super().validate(attrs)

    class Meta:
        model = TimeSlot
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    used_session_count = serializers.IntegerField(read_only=True)
    teacher_name = serializers.CharField(read_only=True)
    students_name = serializers.ListField(read_only=True)
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    def create(self, validated_data):
        students = validated_data.pop("students", [])

        course = Course.objects.create(**validated_data)
        course.students.set(students)

        return course

    class Meta:
        model = Course
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
