from django.db import models
from member.models import Teacher, Student

'''
>>> from django.db.models import Q
>>> Course.objects.filter(Q(start_time__gte="09:00") | Q(end_time__lte='11:00'))
<QuerySet [<Course: Python 101 with Patrick on FRIDAY>]>
'''

'''
TimeSlot -> Course; Course -< TimeSlot

'''


WEEKDAYS = [
    ('SUNDAY', 'sunday'),
    ('MONDAY', 'monday'),
    ('TUESDAY', 'tuesday'),
    ('WEDNESDAY', 'wednesday'),
    ('THRUSDAY', 'thrusday'),
    ('FRIDAY','friday'),
    ('SATURDAY', 'saturday')
]

PRESENT_STATUS = [
    ('PRESENT', 'present'),
    ('EXCUSE', 'excuse'),
    ('SICK LEAVE', 'sick leave'),
    ('ABSENT', 'absent')
]

class Room(models.Model):
    name = models.CharField(max_length=100)

    @property
    def display_name(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

class TimeSlotManager(models.Manager):
    def check_available(self, start_time, end_time, weekdays, room) -> bool: #True if there isn't
        return self.filter(
            models.Q(weekday=weekdays) & 
            models.Q(room=room) & 
            models.Q(start_time__lte=end_time) & 
            models.Q(end_time__gte=start_time) 
        )

class Subject(models.Model):
    topic = models.CharField(max_length=100)
    objective = models.TextField()
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.topic

class Curriculum(models.Model):
    name = models.CharField(max_length=100) 
    subjects = models.ManyToManyField(Subject, null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    weekday = models.CharField(choices=WEEKDAYS, max_length=9)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="time_slots")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name="time_slots")
    objects = TimeSlotManager()

    @property
    def room_name(self):
        return self.room.display_name

    def __str__(self):
        return f"{self.weekday}, {self.start_time}:{self.end_time}, {[i.name for i in self.course_set.all()]}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    deduct_credit = models.IntegerField()
    active = models.BooleanField(default=True)
    max_session = models.IntegerField(default=10)
    time_slots = models.ManyToManyField(TimeSlot, null=True, blank=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True)

    # objects = CourseManager()

    @property
    def used_session_count(self):
        return self.sessions.count()

    @property
    def teacher_name(self):
        return self.teacher.display_name

    @property
    def room_name(self):
        return self.room.name

    @property
    def curriculum_name(self):
        return self.curriculum.name

    @property
    def display_time_slot(self):
        return [(f"{time_slot.start_time}-{time_slot.end_time} on {str(time_slot.weekday).capitalize()} at {time_slot.room.name}") for time_slot in self.time_slots.all()]

    @property
    def students_name(self):
        return [student.get_name for student in self.students.all()]
        # return [student.registered_individual.first_name for student in self.students.all()]

    def __str__(self):
        return f"{self.name} with {self.teacher}"

class Session(models.Model):
    course = models.ForeignKey(Course, related_name="sessions", on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)

    def __update_course_status(self):
        self.course.active = self.course.max_session > self.course.sessions.count()
        self.course.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__update_course_status()

    def __str__(self):
        return f"{self.course} @ {self.date_time}"

class Attendance(models.Model):
    session = models.ForeignKey(Session, related_name='attendances', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='attendances', on_delete=models.CASCADE)
    status = models.CharField(choices=PRESENT_STATUS, null=True)
    comment = models.TextField()

    # def save(self, *args, **kwargs):
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session} > {self.student}"