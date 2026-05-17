from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

#class Parent(models.Model):

class Student(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    current_credit = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class CreditTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    credit = models.IntegerField()
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} | {self.note}"
