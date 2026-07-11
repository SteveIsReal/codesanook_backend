from django.contrib import admin
from member.models import *


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ['current_credit']

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass