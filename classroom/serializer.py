from rest_framework import serializers
from classroom.models import *

class CourseSerializer(serializers.ModelSerializer):

    # teacher = serializers.SerializerMethodField()
    # students = serializers.SerializerMethodField()
    # room = serializers.SerializerMethodField()

    # def get_teacher(self, obj):
    #     return obj.teacher.user.first_name

    # def get_students(self, obj):
    #     return [i.name for i in obj.students.all()]

    # def get_room(self, obj):
    #     return obj.room.name

    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    used_session_count = serializers.IntegerField(read_only=True)
    teacher_name = serializers.CharField(read_only=True)
    students_name = serializers.ListField(read_only=True)
    room_name = serializers.CharField(read_only=True)

    """ 
    def to_representation(self, instance):
        represention = super().to_representation(instance) 

        # represention['teacher'] = instance.teacher.display_name if instance.teacher else None
        represention['students'] = [student.name for student in instance.students.all()]
        represention['room'] = instance.room.name if instance.room else None

        print("111111")
        print(represention)

        return represention
    """

    def validate(self, attrs):
        available_qs = Course.objects.check_available(
                             start_time=attrs['start_time'], 
                             end_time=attrs['end_time'],
                             weekdays=attrs['weekday'],
                             room=attrs['room']
                             )
        if self.instance:
            available_qs = available_qs.exclude(id=self.instance.id)

        if available_qs.exists():
            raise serializers.ValidationError({'info' : [str(i) for i in available_qs],'status':400})

        return super().validate(attrs)

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