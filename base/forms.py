from django.forms import ModelForm
from .models import Employee
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


        