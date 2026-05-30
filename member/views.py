from rest_framework import viewsets
from django.contrib.auth.models import User
from member.models import *
from member.serializers import *

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer