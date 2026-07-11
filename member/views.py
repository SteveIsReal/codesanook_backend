from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from django.contrib.auth.models import User
from member.models import *
from member.serializers import *

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AddCreditView(CreateAPIView):
    queryset = CreditTransaction.objects.all()
    serializer_class = AddCreditTrasactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context() 
        context['request'] = self.request
        return context

class UseCreditView(CreateAPIView):
    queryset = CreditTransaction.objects.all()
    serializer_class = UseCreditTransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ListCreditView(ListAPIView):
    serializer_class = CreditTransactionSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')

        return CreditTransaction.objects.filter(student=student_id)

class ListSchoolView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
