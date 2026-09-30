from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classroom.views import *

router = DefaultRouter()
router.register("room", RoomViewset)
router.register("course", CouseViewset)
router.register("time_slot", TimeSlotViewset)
router.register("subject", SubjectViewset)
router.register("curriculum", CurriculumViewset)
router.register("session", SessionViewset)
router.register("attendance", AttendanceViewset)

urlpatterns = [
    path('', include(router.urls))
]