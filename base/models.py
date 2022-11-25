from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from django.urls import reverse


    
class Employee(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	mobile_number = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True, unique=True)
	profile_picture = models.ImageField(default="default_profile.png", null=True, blank=True)

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
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

