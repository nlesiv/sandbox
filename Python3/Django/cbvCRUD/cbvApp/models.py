from django.db import models
from django.urls import reverse

# Create your models here.
class Student(models.Model):
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    testScore = models.FloatField()

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    