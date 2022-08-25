from django.db import models
from django.utils import timezone
from .config import GENDER_CHOICE


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    phone_number = models.IntegerField()
    email = models.EmailField()
    address = models.TextField(max_length=100)
    date_of_joining = models.DateField()
    salary = models.IntegerField()
    subject = models.CharField(max_length=10)
    previous_organization = models.CharField(max_length=30)
    created_dtm = models.DateTimeField(default=timezone.now)
    updated_dtm = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "teacher"
