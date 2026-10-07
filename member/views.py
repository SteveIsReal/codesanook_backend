from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from member.models import *
from member.serializers import *
from member.filters import StudentFilter

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilter

    def paginate_queryset(self, queryset):
        if "is_student" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

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
    pagination_class = None
    
