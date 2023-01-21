from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(unique=False)
    present = models.BooleanField()
