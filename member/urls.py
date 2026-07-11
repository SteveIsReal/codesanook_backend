from django.urls import path, include
from rest_framework.routers import DefaultRouter
from member.views import *

router = DefaultRouter()
router.register('teacher', TeacherViewset)
router.register('user', UserViewset)
router.register('student', StudentViewset)

urlpatterns = [
    path('add_credit/', AddCreditView.as_view()),
    path('use_credit/', UseCreditView.as_view()),
    path('view_credit/<int:student_id>/', ListCreditView.as_view()),
    path('get_school/', ListSchoolView.as_view()),
    path('', include(router.urls)),
]