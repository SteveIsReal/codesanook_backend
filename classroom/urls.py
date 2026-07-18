from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classroom.views import *

router = DefaultRouter()
router.register("room", RoomViewset)
router.register("course", CouseViewset)

urlpatterns = [
    path('', include(router.urls))
]