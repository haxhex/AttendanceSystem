from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class In_Out(models.Model):
    in_time = models.TimeField()
    out_time = models.TimeField()
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
    )
