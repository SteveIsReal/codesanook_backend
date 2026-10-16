from django.db import models
from django.contrib.auth import get_user_model
from .constant import RELATIONSHIP, GRADE, WEEKDAYS
from datetime import date


User = get_user_model()

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def display_name(self):
        return self.user.first_name

    def __str__(self):
        return f"{self.user.username}"

#class Parent(models.Model):

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)

    grade = models.CharField(choices=GRADE, max_length=14, null=True) #non none
    register_date = models.DateField(auto_now=True)
    birthday = models.DateField(null=True) #non none
    interested_course = models.ManyToManyField("classroom.Curriculum")

    WEEKDAYS
    available_day = models.JSONField(default=list)
    available_schedule = models.ManyToManyField("classroom.Schedule")
    acquaint = models.CharField(max_length=100, null=True)   
    recommender = models.CharField(max_length=100, null=True, blank=True)

    parent_first_name = models.CharField(max_length=100, null=True)
    parent_last_name = models.CharField(max_length=100, null=True)
    relationship = models.CharField(max_length=6, choices=RELATIONSHIP,null=True)
    career = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    id_line = models.CharField(max_length=100, null=True)

    approve = models.BooleanField(default=False)

    @property
    def get_name(self):
        return f"{self.nickname}, {self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        year_diff = today.year - self.birthday.year
        had_not_birthday_yet = (today.month, today.day) < (self.birthday.month, self.birthday.day)

        return year_diff - had_not_birthday_yet

    def __str__(self):
        return f"{self.get_name}"

class Student(models.Model):
    lead = models.ForeignKey(Lead, related_name="student", on_delete=models.CASCADE, null=True)
    current_credit = models.IntegerField(default=0)

    @property
    def get_name(self):
        # return f"{self.lead.nickname}, {self.lead.first_name} {self.lead.last_name}"
        return f"{self.lead}"

    def __str__(self):
        return f"{self.get_name}"

class CreditTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    credit = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    #exp 

    def recalculate_credit(self):
        current_credit = sum([i.credit for i in CreditTransaction.objects.filter(student=self.student)])
        student = self.student
        student.current_credit = current_credit
        student.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recalculate_credit()

    def __str__(self):
        return f"{self.student} | {self.note}"

    class Meta:
        ordering = ['-date_time']
