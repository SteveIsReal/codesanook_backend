from django.db import models
from member.models import Teacher, Student


WEEKDAYS = [
    ('SUNDAY', 'sunday'),
    ('MONDAY', 'monday'),
    ('TUESDAY', 'tuesday'),
    ('WEDNESDAY', 'wednesday'),
    ('THRUSDAY', 'thrusday'),
    ('FRIDAY','friday'),
    ('SATURDAY', 'saturday')
]

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    weekday = models.CharField(choices=WEEKDAYS, max_length=9)
    deduct_credit = models.IntegerField()
    active = models.BooleanField(default=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_session = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name} with {self.teacher} on {self.weekday}"

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __update_course_status(self):
        self.course.active = self.course.max_session > self.course.session_set.count()
        self.course.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__update_course_status()

    def __str__(self):
        return f"{self.course} @ {self.date_time}"

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.session} > {self.student}"