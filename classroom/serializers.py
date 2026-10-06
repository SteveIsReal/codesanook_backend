from rest_framework import serializers
from classroom.models import *


class TimeSlotSerializer(serializers.ModelSerializer):

    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_name = serializers.CharField(read_only=True)
    time = serializers.ListField()

    def validate(self, attrs):
        avaliable_qs = TimeSlot.objects.check_available(
            start_time=attrs['start_time'],
            end_time=attrs['end_time'],
            weekdays=attrs['weekday'],
            room=attrs['room']
        )

        if self.instance:
            avaliable_qs = avaliable_qs.exclude(id=self.instance.id)

        if avaliable_qs.exists():
            print("1111111")
            raise serializers.ValidationError({"info": "nah"})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        time = validated_data.pop("time", [])

        if time:
            instance.start_time = time[0]
            instance.end_time = time[1]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        time = validated_data.pop("time", [])
        return super().create(validated_data)

    class Meta:
        model = TimeSlot
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    students_obj = serializers.SerializerMethodField()
    time_slots = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all(), many=True)
    used_session_count = serializers.IntegerField(read_only=True)
    teacher_name = serializers.CharField(read_only=True)
    curriculum_name = serializers.CharField(read_only=True)
    display_time_slot = serializers.ListField(read_only=True)


    def create(self, validated_data):
        students = validated_data.pop("students", [])
        time_slots = validated_data.pop("time_slots", [])

        course = Course.objects.create(**validated_data)
        course.students.set(students)
        course.time_slots.set(time_slots)

        return course

    def get_students_obj(self, obj):
        from member.serializers import StudentSerializer
        return StudentSerializer(obj.students.all(), many=True).data

    class Meta:
        model = Course
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subject
        fields = "__all__"

class CurriculumSerializer(serializers.ModelSerializer):

    subjects = SubjectSerializer(many=True)

    def create(self, validated_data):
        subjects_data = validated_data.pop("subjects", [])
        curriculum = Curriculum.objects.create(**validated_data)

        for subject_data in subjects_data:
            subject = Subject.objects.create(**subject_data)
            curriculum.subjects.add(subject)

        return curriculum

    def update(self, instance, validated_data):
        print(validated_data)
        subjects_data = validated_data.pop("subjects", [])

        instance.name = validated_data['name']
        instance.save()

        current_subject = {subject.id : subject for subject in instance.subjects.all()}
        new_subject = []

        for subject_data in subjects_data:
            print(subject_data.get("id"))
            subject_id = subject_data.get("id", False)
            if subject_id:
                subject = current_subject.get(subject_id)
                print('same', subject)
                if subject:
                    subject.topic = subject_data.get('topic', subject.topic)
                    subject.objective = subject_data.get('objective', subject.objective)
                    subject.save()
                    new_subject.append(subject)
            else:
                print('new')
                subject = Subject.objects.create(**subject_data)
                new_subject.append(subject)

        instance.subjects.set(new_subject)

        return instance 

    class Meta:
        model = Curriculum
        fields = "__all__"

class SessionSerializer(serializers.ModelSerializer):
    time_slot_obj = serializers.SerializerMethodField()
    subject_obj = serializers.SerializerMethodField()
    students_info = serializers.SerializerMethodField(read_only=True)

    def get_students_info(self, obj):
        return [AttendanceSerializer(attendance).data for attendance in obj.attendances.all()]

    def get_subject_obj(self, obj):
        return SubjectSerializer(obj.subject).data

    def get_time_slot_obj(self, obj):
        return TimeSlotSerializer(obj.time_slot).data

    class Meta:
        model = Session
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):

    student_obj = serializers.SerializerMethodField()

    def get_student_obj(self, obj):
        from member.serializers import StudentSerializer
        return StudentSerializer(obj.student).data

    def create(self, validated_data):
        from member.models import CreditTransaction
        attendance = Attendance.objects.create(**validated_data)
        if attendance.status == "PRESENT" or attendance.status == "ABSENT":
            credit_transaction = CreditTransaction.objects.create(
                student=attendance.student, 
                credit=-attendance.session.course.deduct_credit,
                note=f"attendance in {attendance.session.course}"
            )
            print(credit_transaction)

        return attendance

    def update(self, instance, validated_data):
        from member.models import CreditTransaction

        old_status = instance.status
        new_status = validated_data.get("status", old_status)

        deduct_statuses = ["PRESENT", "ABSENT"]

        old_should_deduct = old_status in deduct_statuses
        new_should_deduct = new_status in deduct_statuses

        instance = super().update(instance, validated_data)

        if not old_should_deduct and new_should_deduct:
            CreditTransaction.objects.create(
                student=instance.student,
                credit=-instance.session.course.deduct_credit,
                note=f"change {old_status} to {new_status}"
            )

        elif old_should_deduct and not new_should_deduct:
            CreditTransaction.objects.create(
                student=instance.student,
                credit=instance.session.course.deduct_credit,
                note=f"change {old_status} to {new_status}"
            )

        return instance

    class Meta:
        model = Attendance
        fields = "__all__"

