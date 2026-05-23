from django.urls import path, include
from rest_framework.routers import DefaultRouter
from member.views import *

router = DefaultRouter()
router.register('teacher', TeacherViewset)

urlpatterns = [
    path('', include(router.urls))
]