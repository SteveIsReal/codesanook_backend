from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

#class Parent(models.Model):

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    current_credit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class CreditTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    credit = models.IntegerField()
    note = models.TextField(null=True, blank=True)

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
