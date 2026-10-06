from django.db import models
from django.contrib.auth import get_user_model

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

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    current_credit = models.IntegerField(default=0)
    is_student = models.BooleanField(default=False, null=True) #Cuz, some of the registered people don't become real student

    @property
    def get_name(self):
        return f"{self.nickname}, {self.first_name} {self.last_name}"

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
