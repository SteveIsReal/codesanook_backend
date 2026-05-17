from django.contrib import admin
from classroom.models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass