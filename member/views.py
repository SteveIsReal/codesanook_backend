from rest_framework import viewsets
from member.models import *
from member.serializers import *

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer