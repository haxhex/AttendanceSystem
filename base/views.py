import calendar
from django.shortcuts import render, redirect, get_object_or_404
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
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.views import generic
from datetime import date, datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
import re
from datetime import datetime as dt
import datetime as dtt
from .utils import get_plot
import xlwt



# User = get_user_model()

def home(request):
    return render(request, 'base/home.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required(login_url='login')
def dashboard(request):
	in_outs = In_out.objects.all()
	in_out_list = []
	for in_out in in_outs:
		if in_out.employee.id == request.user.employee.id:
			in_out_list.append(in_out)
	
	return render(request ,'base/dashboard.html', {'in_outs' : in_out_list})

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
@allowed_users(allowed_roles=['admin'])
def employees_list(request):
    employees = Employee.objects.all()
    employees_list = []
    for employee in employees:
        if employee.user.id != request.user.id:
            employees_list.append(employee) 
    context = {'employees' : employees_list, 'fltr':'all'}
    return render(request, 'base/employees_list.html', context)


@login_required(login_url='login')
def view_profile(request):
    return render(request, 'base/view_profile.html')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.new_password1 = request.POST.get('new_password1')
            form.new_password2 = request.POST.get('new_password2')
            form.save()
            # new_password1 = request.POST.get('new_password1')
            # new_password2 = request.POST.get('new_password2')
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
			# data = password_reset_form.cleaned_data['email']
			data = request.POST.get('email')
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
	valid_username = True
	emailvalue=''
	uservalue=''
	passwordvalue1=''
	passwordvalue2=''
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		print("Form Created")
		uservalue = request.POST.get('username')
		emailvalue = request.POST.get('email')
		passwordvalue1 = request.POST.get('password1')
		passwordvalue2 = request.POST.get('password2')
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		if passwordvalue1 == passwordvalue2:
			print("----Password Matched")
			if passwordvalue1 == uservalue:
				context= {'form': form, 'error':'Your password can’t be too similar to your other personal information. Please try another password.'}
				print("----Password match username")
				return render(request, 'base/sign-up.html', context)
			if len(passwordvalue1) < 8:
				context= {'form': form, 'error':'Your password must contain at least 8 characters. Please try another password.'}
				print("----Password is too short")
				return render(request, 'base/sign-up.html', context)
			if not re.match('.*[0-9]', passwordvalue1):
				print("---Your password must contain a number")
				context= {'form': form, 'error':'Your password must contain a number. Please try another password.'}
				return render(request, 'base/sign-up.html', context)
			if not re.match('.*[A-Z]', passwordvalue1):
				print("---Your password must contain at least 1 upper case character.")
				context= {'form': form, 'error':'Your password must contain at least 1 upper case character. Please try another password.'}
				return render(request, 'base/sign-up.html', context)
			if not re.match('.*[a-z]', passwordvalue1):
				print("Your password must contain at least 1 lower case character." )
				context= {'form': form, 'error':'Your password must contain at least 1 lower case character. Please try another password.'}
				return render(request, 'base/sign-up.html', context)			
			try:
				user= User.objects.get(username=uservalue)
				context= {'form': form, 'error':'The username you entered has already been taken. Please try another username.'}
				print("----User Exist")
				return render(request, 'base/sign-up.html', context)
			except User.DoesNotExist:
				print("-----User Not Exist")
				try:
					user= User.objects.get(email=emailvalue)
					context= {'form': form, 'error':'The email you entered has already been taken. Please try another email.'}
					return render(request, 'base/sign-up.html', context)
				except:
					print("Email not repeated")
          			
					if form.is_valid():
						print("----Form is Valid")
						user = form.save()
						username = request.POST.get('username')
						email = request.POST.get('email')
						first_name = request.POST.get('first_name')
						last_name = request.POST.get('last_name')
						group = Group.objects.get(name='employee')
						user.groups.add(group)
						Employee.objects.create(
							user = user,
							email = email,
							first_name = first_name,
							last_name = last_name
						)
						context= {'form': form}
						messages.success(request, 'Account was created for ' + username)
						valid_username = False
						return redirect('login')
		else:
			print("---Password not match")
			context= {'form': form, 'error':'The passwords that you provided don\'t match'}
			return render(request, 'base/sign-up.html', context)
		if valid_username:
			print("---Invalid Username")
			context= {'form': form, 'error':'Please enter a valid username.\n150 characters or fewer. Letters, digits and @/./+/-/_ only.'}
			return render(request, 'base/sign-up.html', context)

   
	context = {'form':form}
	return render(request, 'base/sign-up.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == "POST":
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				# messages.info(request, f"You are now logged in as {username}.")
				return redirect("dashboard")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = LoginForm()
	context={"form":form}
	return render(request, "base/log-in.html", context)

@login_required(login_url='login')
def accountSettings(request):
	page = 'accountSettings'
	employee = request.user.employee
	form = EmployeeForm(instance=employee)

	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			form.save()
			return redirect('view-profile')
	context = {'form':form, 'page':page}
	return render(request, 'base/edit_profile.html', context)


class CalendarView(generic.ListView):
    model = In_out
    template_name = 'base/calendar.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user_id = self.request.user.employee
        cal = Calendar(d.year, d.month)
        in_outs = In_out.objects.all()
        in_out_list = []
        dates_ss = []
        for in_out in in_outs:
            if in_out.employee.id == self.request.user.employee.id:
                in_out_list.append(in_out)
                if str(in_out.start_time.date()) not in dates_ss:
                   dates_ss.append(str(in_out.start_time.date()))
        t_vals = []
        for dte in dates_ss:   
            total = []
            for in_out in in_outs:    
                if in_out.employee.id == self.request.user.employee.id:
                   if str(in_out.start_time.date()) == dte:
                       FMT = '%H:%M:%S'
                       tdelta = dt.strptime(str(in_out.end_time.time()), FMT) - dt.strptime(str(in_out.start_time.time()), FMT)
                       total.append(str(tdelta))
            mysum = dtt.timedelta()
            for i in total:
                (h, m, s) = i.split(':')
                dd = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                mysum += dd
            date_time = dtt.datetime.strptime(str(mysum), "%H:%M:%S")
            t_vals.append(date_time)    
        chart = get_plot(dates_ss, t_vals)
        html_cal = cal.formatmonth(user_id, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['chart'] = chart
        return context
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, inOut_id=None):
    instance = In_out()
    if inOut_id:
        instance = get_object_or_404(Event, pk=inOut_id)
    else:
        instance = In_out()

    form = InOutForm(request.POST or None,instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'base/event.html', {'form': form})

def handle_not_found(request, exception):
    return render(request, 'base/not-found.html')

def createUser(request):
    return render(request, 'base/create-user.html')


def createUser(request):
	valid_username = True
	emailvalue=''
	uservalue=''
	passwordvalue1=''
	passwordvalue2=''
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		print("Form Created")
		uservalue = request.POST.get('username')
		emailvalue = request.POST.get('email')
		passwordvalue1 = request.POST.get('password1')
		passwordvalue2 = request.POST.get('password2')
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		if passwordvalue1 == passwordvalue2:
			print("----Password Matched")
			if passwordvalue1 == uservalue:
				context= {'form': form, 'error':'Your password can’t be too similar to your other personal information. Please try another password.'}
				print("----Password match username")
				return render(request, 'base/create-user.html', context)
			if len(passwordvalue1) < 8:
				context= {'form': form, 'error':'Your password must contain at least 8 characters. Please try another password.'}
				print("----Password is too short")
				return render(request, 'base/create-user.html', context)
			if not re.match('.*[0-9]', passwordvalue1):
				print("---Your password must contain a number")
				context= {'form': form, 'error':'Your password must contain a number. Please try another password.'}
				return render(request, 'base/create-user.html', context)
			if not re.match('.*[A-Z]', passwordvalue1):
				print("---Your password must contain at least 1 upper case character.")
				context= {'form': form, 'error':'Your password must contain at least 1 upper case character. Please try another password.'}
				return render(request, 'base/create-user.html', context)
			if not re.match('.*[a-z]', passwordvalue1):
				print("Your password must contain at least 1 lower case character." )
				context= {'form': form, 'error':'Your password must contain at least 1 lower case character. Please try another password.'}
				return render(request, 'base/create-user.html', context)			
			try:
				user= User.objects.get(username=uservalue)
				context= {'form': form, 'error':'The username you entered has already been taken. Please try another username.'}
				print("----User Exist")
				return render(request, 'base/create-user.html', context)
			except User.DoesNotExist:
				print("-----User Not Exist")
				try:
					user= User.objects.get(email=emailvalue)
					context= {'form': form, 'error':'The email you entered has already been taken. Please try another email.'}
					return render(request, 'base/create-user.html', context)
				except:
					print("Email not repeated")
          			
					if form.is_valid():
						print("----Form is Valid")
						user = form.save()
						username = request.POST.get('username')
						email = request.POST.get('email')
						first_name = request.POST.get('first_name')
						last_name = request.POST.get('last_name')
						group = Group.objects.get(name='employee')
						user.groups.add(group)
						Employee.objects.create(
							user = user,
							email = email,
							first_name = first_name,
							last_name = last_name
						)
						context= {'form': form}
						messages.success(request, 'Account was created for ' + username)
						valid_username = False
						return redirect('employees_list')
		else:
			print("---Password not match")
			context= {'form': form, 'error':'The passwords that you provided don\'t match'}
			return render(request, 'base/create-user.html', context)
		if valid_username:
			print("---Invalid Username")
			context= {'form': form, 'error':'Please enter a valid username.\n150 characters or fewer. Letters, digits and @/./+/-/_ only.'}
			return render(request, 'base/create-user.html', context)
	   
	context = {'form':form}
	return render(request, 'base/create-user.html', context)

def editUser(request, pk):
	page = 'editUser'
	employee = Employee.objects.get(id=pk)
	form = EmployeeForm(instance=employee)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			form.save()
			return redirect('employees_list')
	context = {'form':form, 'eid': pk, 'page':page}
	return render(request, 'base/edit-user.html', context)


def changeUserPass(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        form = SetPasswordForm(employee.user, request.POST)
        if form.is_valid():
            form.new_password1 = request.POST.get('new_password1')
            form.new_password2 = request.POST.get('new_password2')
            form.save()
            messages.success(request, f"{employee.first_name} {employee.last_name} password has been changed successfully!")
            # return redirect('edit-user', pk=pk)
            return redirect('employees_list')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(employee.user)
    return render(request, 'base/password_reset_confirm.html', {'form': form})


def deleteUser(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        # remove item from database
        employee.user.delete()
        return redirect('employees_list')
    return render(request, 'base/delete.html', {'obj' :  employee.user})

def change_status(request, pk):
	employee = Employee.objects.get(id=pk)
	employee.user.is_active = not employee.user.is_active
	employee.user.save()
	return redirect('employees_list')

def export_excel(request, fltr):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Employees_List ' + \
		str(dtt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Employees')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Firstname', 'Lastname', 'Email' ,'Mobile Number', 'Status']
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	
	font_style = xlwt.XFStyle()
	rows = Employee.objects.all().values_list(
		'first_name', 'last_name', 'email', 'mobile_number'
	)
	rows1 = Employee.objects.all()
	emps_status = []
	for r in rows1:
		if r.user.is_active:
			emps_status.append('Active')
		else:
			emps_status.append('Inactive')
	print(emps_status)
	snum = 0
	r_a = 1
	for row in rows:
		row_num += 1
		for col_num in range(len(row)+1):
			if fltr == 'saf':
				if emps_status[snum] == 'Active':
					if col_num == 4:
						ws.write(row_num, col_num, 'Active', font_style)
						snum += 1
					else:
						ws.write(row_num, col_num, str(row[col_num]), font_style)
				else:
					if col_num == 4:
						snum += 1 
						row_num -= 1
			elif fltr == 'sif':
				if emps_status[snum] == 'Inactive':
					if col_num == 4:
						ws.write(row_num, col_num, 'Inactive', font_style)
						snum += 1
					else:
						ws.write(row_num, col_num, str(row[col_num]), font_style)
				else:
					if col_num == 4:
						snum += 1 
						row_num -= 1
			else:
				if col_num == 4:
					ws.write(row_num, col_num, str(emps_status[snum]), font_style)
					snum += 1
				else:
					ws.write(row_num, col_num, str(row[col_num]), font_style)
	wb.save(response)
	return response

def status_active_filter(request):
    employees = Employee.objects.all()
    employees_list = []
    for employee in employees:
        if employee.user.is_active and employee.user.id != request.user.id:
            employees_list.append(employee)  
    context = {'employees' : employees_list, 'fltr':'saf'}
    return render(request, 'base/employees_list.html', context) 

def status_inactive_filter(request):
    employees = Employee.objects.all()
    employees_list = []
    for employee in employees:
        if not employee.user.is_active and employee.user.id != request.user.id:
            employees_list.append(employee) 
    context = {'employees' : employees_list, 'fltr':'sif'}
    return render(request, 'base/employees_list.html', context)         
     
 
	