from rest_framework import serializers
from member.models import *

class TeacherSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source = "user.first_name")
    last_name = serializers.CharField(source = "user.last_name")
    email = serializers.CharField(source = "user.email")

    class Meta:
        model = Teacher
        fields = "__all__"