from django.db import models
from django.contrib.auth.models import User
import datetime

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    # password = models.CharField(max_length=20)
    def __str__(self):
        return str(self.user)


class In_out(models.Model):
    date = models.DateField(default=datetime.date.today)
    in_time = models.TimeField()
    out_time = models.TimeField()
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
    )
