from django.db import models
from django.conf import settings
# Create your models here.
class Student(models.Model):
    name  = models.CharField(max_length=50)
    mssv  = models.CharField(max_length=8)
    Class = models.CharField(max_length=60, default="KSTN-CNTT-K63")
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.name + " " + self.mssv + " " + self.Class + " " + str(self.status)