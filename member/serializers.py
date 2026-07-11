from rest_framework import serializers
from member.models import *
from classroom.serializer import CourseSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email','password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

class TeacherSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source = "user.username", read_only=True)
    first_name = serializers.CharField(source = "user.first_name", read_only=True)
    last_name = serializers.CharField(source = "user.last_name", read_only=True)
    email = serializers.CharField(source = "user.email", read_only=True)
    user = UserSerializer()
    
    def create(self, vaildated_data):
        user_data = vaildated_data.pop("user")

        user_instance = User.objects.create(**user_data)
        teacher_instance = Teacher.objects.create(user=user_instance)

        return teacher_instance

    def update(self, instance, vaildated_data):
        teacher_data = vaildated_data.pop('user', {})
        user = instance.user

        for attr, value in teacher_data.items():
            setattr(user, attr, value)

        user.save()

        return super().update(instance, vaildated_data)

    class Meta:
        model = Teacher
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):

    course = serializers.SerializerMethodField()

    def get_course(self, obj):
        #return CourseSerializer(obj.course_set.all(), many=True).data
        return [c.name for c in obj.course_set.all()]

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ['current_credit']

class CreditTransactionSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date_time.strftime('%d/%m/%Y')

    def get_time(self, obj):
        return obj.date_time.strftime('%H:%M')

    class Meta:
        model = CreditTransaction
        fields = "__all__"
        read_only_fields = ['date_time']

class AddCreditTrasactionSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['credit'] <= 0:
            raise serializers.ValidationError({
                'credit' : "credit must be more than 0"
            })
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        print(request.user)

        validated_data['note'] = f"{request.user} added {validated_data["credit"]} credit"

        return super().create(validated_data)

    class Meta:
        model = CreditTransaction
        fields = "__all__"
        read_only_fields = ['date_time']

class UseCreditTransactionSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['credit'] >= 0:
            raise serializers.ValidationError({
                'credit' : "credit must be less than 0"
            })
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['note'] = f"{request.user} removed {validated_data['credit'] * -1} credits"
        return super().create(validated_data)

    class Meta:
        model = CreditTransaction
        fields = "__all__"
        read_only_fields = ['date_time']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"