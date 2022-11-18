from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout , get_user_model
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth. forms import UserCreationForm
from .forms import *
from django.http import HttpResponse
from .models import *
from .forms import SetPasswordForm
from .forms import PasswordResetForm
from .forms import PasswordResetForm
from django.db.models.query_utils import Q
from typing import Protocol
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import *
from .decorators import user_not_authenticated
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# User = get_user_model()

def home(request):
    return render(request, 'base/home.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    in_outs = In_out.objects.all()
    context = {'in_outs' : in_outs}
    return render(request ,'base/dashboard.html', context)

@login_required(login_url='login')
def io(request):
    return render(request ,'base/io.html')

@login_required(login_url='login')
def io_archive(request):
    return render(request ,'base/io_archive.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def io_report(request):
    return render(request ,'base/io_report.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def io_archive_report(request):
    return render(request ,'base/io_archive_report.html')

@login_required(login_url='login')
def view_profile(request):
    return render(request, 'base/view_profile.html')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'base/password_reset_confirm.html', {'form': form})


@user_not_authenticated
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "base/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="base/password_reset.html", context={"password_reset_form":password_reset_form})

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			group = Group.objects.get(name='employee')
			user.groups.add(group)
			Employee.objects.create(
				user=user,
				email=email,
                first_name = first_name,
                last_name = last_name
    )

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'base/login_register.html', context)

@unauthenticated_user
def loginPage(request):
	page = 'login'
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {'page': page}
	return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def accountSettings(request):
	employee = request.user.employee
	form = EmployeeForm(instance=employee)

	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			form.save()
			return redirect('view-profile')
	context = {'form':form}
	return render(request, 'base/edit_profile.html', context)