from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from django.urls import reverse

def mentor_photos(instance, filename):
    return 'mentor/photos/%s' % filename


    
class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    profile_picture = models.ImageField(default="default_profile.png", null=True, blank=True, upload_to=mentor_photos)	
    department = models.CharField(max_length=200, null=True)	
    position = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.user)


class In_out(models.Model):
    start_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(default=datetime.datetime.now)
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
    )
    @property
    def get_html_url(self):
        # url = reverse('event_edit', args=(self.id,))
        # return f'<a href="{url}"> {self.start_time} <br/> {self.end_time} </a>'
        return f'Time In: {self.start_time.time().strftime("%H:%M:%S")} <br/> Time Out: {self.end_time.time().strftime("%H:%M:%S")}'
    
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
class Position(models.Model):
    name =  models.CharField(max_length=200, null=True)
    department =  models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.name)
    @property
    def get_html_url(self):
        # url = reverse('event_edit', args=(self.id,))
        # return f'<a href="{url}"> {self.start_time} <br/> {self.end_time} </a>'
        return f'Department: {self.name} <br/> Position: {self.department}'

