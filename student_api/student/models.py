from django.db import models
from django.utils import timezone
from .config import GENDER_CHOICE, MODE_OF_STAY_CHOICE


class Student(models.Model):

    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    sibilings = models.IntegerField()
    address = models.TextField(max_length=100)
    parent_mobile = models.IntegerField()
    date_of_joining = models.DateField()
    mode_of_stay = models.CharField(choices=MODE_OF_STAY_CHOICE, max_length=20)
    fees = models.IntegerField()
    class_teacher_id = models.IntegerField(null=True, blank=True, default=0)
    created_dtm = models.DateTimeField(default=timezone.now)
    updated_dtm = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "student"
