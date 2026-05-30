from rest_framework import serializers
from member.models import *
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

