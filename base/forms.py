from django.forms import ModelForm
from .models import Employee
from django.contrib.auth.forms import SetPasswordForm , UserCreationForm ,AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.forms import ModelForm, DateInput
from base.models import Event
from django import forms

Positions =[
            (' ', 'Select your position'),
            ('Accounting', (
                    ('Auditor', 'Auditor'),
                    ('CFO', 'CFO'),
                    ('Payroll specialist', 'Payroll specialist'),
                    ('Tax specialist', 'Tax specialist'),       
                )
            ),
            ('Marketing', (
                    ('Advertising manager', 'Advertising manager'),
                    ('Brand manager', 'Brand manager'),
                    ('Public relations officer', 'Public relations officer'),
                    ('Market analyst', 'Market analyst'),           
                )
            ),
            ('Human resources', (
                    ('Compensation specialist', 'Compensation specialist'),
                    ('Brand manager', 'Brand manager'),
                    ('Personnel manager', 'Personnel manager'),
                    ('Market analyst', 'Market analyst'),
                    ('Recruiter', 'Recruiter'),  
                    ('Training manager', 'Training manager'),                             
                )
            ),
            ('Production', (
                    ('Chief inspector', 'Chief inspector'),
                    ('Brand manager', 'Brand manager'),
                    ('Market analyst', 'Market analyst'),
                    ('Recruiter', 'Recruiter'),  
                    ('Machinist', 'Machinist'), 
                    ('Plant manager', 'Plant manager'), 
                    ('Quality control manager ', 'Quality control manager'), 
                                                
                )
            ),
            
            ('IT', (
                    ('Communications analyst', 'Communications analyst'),
                    ('Database administrator', 'Database administrator'),
                    ('E_business specialist', 'E-business specialist'),
                    ('PC support specialist', 'PC support specialist'), 
                    ('Programmer', 'Programmer'),
                    ('Site manager', 'Site manager'),                                        
                )
            ),
            ('Sales', (
                    ('Branch manager', 'Branch manager'),
                    ('Retail manager', 'Retail manager'),
                    ('Telemarketer', 'Telemarketer'),                                        
                )
            ),
    
        ]     

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name' ,'email','mobile_number','profile_picture','position']
        widgets = {
            
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number' : forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'position': forms.Select(choices=Positions,attrs={'class': 'form-control'}),
        }
        

    
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
# class EmployeeForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     mobile_number = forms.EmailField(required=False)
#     profile_picture = forms.ImageField(required=False)
#     position = forms.Select(choices=Positions,attrs={'class': 'form-control'})

#     class Meta:
#         model = Employee
#         fields = ('first_name', 'last_name' ,'email' , 'mobile_number' , 'profile_picture' , 'position' )
#         exclude = ['user', 'is_active', 'department']
#         widgets = {
#             'position': forms.Select(choices=Positions,attrs={'class': 'form-control'}),
#         }

#     def clean_email(self):
#         username = self.cleaned_data.get('username')
#         email = self.cleaned_data.get('email')

#         if email and User.objects.filter(email=email).exclude(username=username).count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email

#     def save(self, commit=True):
#         user = super(UserRegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']

#         if commit:
#             user.save()

#         return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
        

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
    label=_("Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control","id": "form3Example4"}),
    help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
    label=_("Password confirmation"),
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control","id": "form3Example5"}),
    strip=False,
    help_text=_("Enter the same password as before, for verification."),
    )
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True  
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','id': 'form3Example0'}),            
            'first_name': forms.TextInput(attrs={'class': 'form-control','id': 'form3Example1'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','id': 'form3Example2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'form3Example3'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control','id': 'form3Example4'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control','id': 'form3Example5'}),    
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','id': 'form3Example3'}),)

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control','id': 'form3Example4'}))
    

class InOutForm(ModelForm):
  class Meta:
    model = In_out
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(InOutForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    

# class FaceForm(ModelForm):
#      class Meta:
#          model = Employee
#          fields = ['face_rec']


class CreatePositionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePositionForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['department'].required = True
    class Meta:
        model = Position
        fields = ['name', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'form3Example0'}),            
        }
    




        