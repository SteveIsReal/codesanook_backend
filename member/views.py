from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from member.models import *
from member.serializers import *
from member.filters import StudentFilter, LeadFilter
from account.authenticate import IsTeacherOrAdminForMutationsElsePublic, IsAdmin, IsTeacherOrAdmin

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"] :
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def paginate_queryset(self, queryset):
        if self.request.query_params.get("pagination", False):
            return None
        return super().paginate_queryset(queryset)

class LeadViewset(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = PublicLeadSerializer
    filterset_class = LeadFilter
    permission_classes = [IsTeacherOrAdminForMutationsElsePublic]
    throttle_classes = [AnonRateThrottle]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return PublicLeadSerializer
        return LeadSerializer

class AddCreditView(CreateAPIView):
    queryset = CreditTransaction.objects.all()
    serializer_class = AddCreditTrasactionSerializer
    permission_classes = [IsAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context() 
        context['request'] = self.request
        return context

class UseCreditView(CreateAPIView):
    queryset = CreditTransaction.objects.all()
    serializer_class = UseCreditTransactionSerializer
    permission_classes = [IsAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ListCreditView(ListAPIView):
    serializer_class = CreditTransactionSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')

        return CreditTransaction.objects.filter(student=student_id)

class ListSchoolView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    
class SchoolViewset(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAdmin]