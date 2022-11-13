from django.db import models


class In_Out(models.Model):
    in_time = models.TimeField()
    out_time = models.TimeField()
    employee = models.ForeignKey(
        "employee.User",
        on_delete=models.CASCADE,
    )
