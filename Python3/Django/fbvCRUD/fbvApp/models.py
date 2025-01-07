from django.db import models

# Create your models here.
class Student(models.Model):
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    testScore = models.FloatField()