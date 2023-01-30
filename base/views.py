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
from django.db.models import Q
from dateutil import rrule, parser
from PIL import Image
import numpy as np
from facerecognition.FaceDetector import *
from facenet_pytorch import MTCNN
import urllib.request



# @login_required(login_url='login')
# def face(request):
# 	context = {'page':'take'}
# 	return render (request , "base/face.html", context)

@login_required(login_url='login')
def face(request):

	if request.method == "GET":
		context = {'page' :'take'}
		return render (request , "base/face.html" , context)
	if request.method == "POST":
		try:
			img = request.POST.get('pic')
			print(img)
			img_name1 = "1.png"
			img_name1 = "static/images/faces/" + img_name1
			urllib.request.urlretrieve(img, img_name1)
			img = Image.open(img_name1).convert('RGB')
			mtcnn = MTCNN()
			fcd = FaceDetector(mtcnn)
			detect = fcd.run(img)
			isFace = fcd.detected
			if isFace == True:
				img_name2 = "2.png"
				img_name2 = "static/images/faces/" + img_name2
				detect.save(img_name2)
				context = {'page':'reg', 'msg':'Your face detected and your picture registered successfully!'} 
				return render (request , "base/face_registered.html", context)
			elif isFace == False:
				context = {'page':'reg', 'msg': 'No face has been detected. Please try a gain!'} 
				return render (request , "base/face.html", context)




		except:			
			context = {'page':'reg', 'msg':"There's problem in face recognition. Please try a gain!"} 
			return render (request , "base/face.html", context)


# User = get_user_model()

# def home(request):
#     return render(request, 'base/home.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

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
	employees_list = []
	employees = Employee.objects.all()
	for employee in employees:
		if employee.user.id != request.user.id:
			employees_list.append(employee) 
            
            
	# sdate = dtt.datetime.strptime(drange.split(' - ')[0], '%Y-%m-%d').date()
	# edate = dtt.datetime.strptime(drange.split(' - ')[1], '%Y-%m-%d').date()
	# date_generated = [sdate + dtt.timedelta(days=x) for x in range(0, (edate-sdate).days+1)]
	working_hours = []
	in_outs = In_out.objects.all()
	names = []
	for emp in employees_list:
		in_out_nums = 0
		for in_out in in_outs:
			if in_out.employee.id == emp.id:
				in_out_nums += 1
		if in_out_nums > 0:
			in_out_list = []
			for in_out in in_outs:
				if in_out.employee.id == emp.id:
					in_out_list.append(in_out)
			if len(in_out_list) > 0:
				timeList = []
				timeList1 = []
				for ins in in_out_list:
					timeList.append(str(ins.start_time.time()))
					timeList1.append(str(ins.end_time.time()))

				mysum1 = dtt.timedelta()
				for i in timeList:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum1 += d
				print(str(mysum1))
				mysum2 = dtt.timedelta()
				for i in timeList1:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum2 += d
					
				print(str(mysum2))

				time = mysum2 - mysum1
				print("----------------")
				print(time)
				print("----------------")
				working_hours.append(time)
    
			names.append(emp.id)
		else:
			working_hours.append("00:00:00")
	# print(working_hours)
	# print(names)
	
 
	

	emps_list = zip(employees_list, working_hours)
	dates = []
	for in_out in in_outs:
		if in_out.start_time.date() not in dates:
			dates.append(str(in_out.start_time.date()))
	min_date = min(dates)
	max_date = max(dates)
	drange = min_date + " - " + max_date
    
	context = {'employees' : emps_list, 'dep' : 'All', 'drange' : drange}
	return render(request ,'base/io_report.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employees_list(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    employees = Employee.objects.filter(
        Q(user__is_active__icontains =q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(department__icontains=q) |
        Q(position__icontains=q) |
        Q(email__icontains=q) |
        Q(mobile_number__icontains=q) |
        Q(user__username__icontains =q)
        )
    # employees = Employee.objects.all()
    employees_list = []
    for employee in employees:
        if employee.user.id != request.user.id:
            employees_list.append(employee)  
    context = {'employees' : employees_list, 'fltra':'All', 'fltrd' : 'All', 'q':q}
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
	er = False
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
		errors = []
		if passwordvalue1 != passwordvalue2:
			# print("---Password not match")
			# context= {'form': form, 'error':'The passwords that you provided don\'t match'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The passwords that you provided don\'t match')	
			# print("----Password Matched")
		if passwordvalue1 == uservalue:
			# context= {'form': form, 'error':'Your password can’t be too similar to your other personal information. Please try another password.'}
			# print("----Password match username")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password can\'t be too similar to your other personal information. Please try another password.')
		if len(passwordvalue1) < 8:
			# context= {'form': form, 'error':'Your password must contain at least 8 characters. Please try another password.'}
			# print("----Password is too short")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 8 characters. Please try another password.')
		if not re.match('.*[0-9]', passwordvalue1):
			# print("---Your password must contain a number")
			# context= {'form': form, 'error':'Your password must contain a number. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain a number. Please try another password.')
		if not re.match('.*[A-Z]', passwordvalue1):
			# print("---Your password must contain at least 1 upper case character.")
			# context= {'form': form, 'error':'Your password must contain at least 1 upper case character. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 1 upper case character. Please try another password.')
		if not re.match('.*[a-z]', passwordvalue1):
			# print("Your password must contain at least 1 lower case character." )
			# context= {'form': form, 'error':'Your password must contain at least 1 lower case character. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 1 lower case character. Please try another password.')			
		try:
			user= User.objects.get(username=uservalue)
			print("User Exist")
			# context= {'form': form, 'error':'The username you entered has already been taken. Please try another username.'}
			# print("----User Exist")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The username you entered has already been taken. Please try another username.')			
		except User.DoesNotExist:
			print("-----User Not Exist")
		try:
			user= User.objects.get(email=emailvalue)
			# context= {'form': form, 'error':'The email you entered has already been taken. Please try another email.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The email you entered has already been taken. Please try another email.')			
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
				position = position = request.POST.get('position')
				department1 = department(position)
				user.groups.add(group)
				Employee.objects.create(
					user = user,
					email = email,
					first_name = first_name,
					last_name = last_name,
					position = position,
					department = department1
				)
				context= {'form': form}
				messages.success(request, 'Account was created for ' + username)
				valid_username = False
				return redirect('login')
		
		if er == False and valid_username and not form.is_valid():
			# print("---Invalid Username")
			# context= {'form': form, 'error':'Please enter a valid username.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Please enter a valid username.')			
	positions = Position.objects.all()
	position_list = []
	for p in positions:
		position_list.append(p)
	if er:
		context= {'form': form, 'errors' : errors, 'positions' : position_list}
		return render(request, 'base/sign-up.html', context)
   
	context = {'form':form, 'positions':positions}
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

def department(position):
    Accounting = ['Auditor', 'CFO', 'Payroll specialist', 'Tax specialist']
    Marketing = ['Advertising manager', 'Brand manager', 'Public relations officer', 'Market analyst']
    HumanResources = ['Compensation specialist', 'Brand manager', 'Personnel manager', 'Market analyst', 'Recruiter', 'Training manager']
    Production = ['Chief inspector', 'Brand manager', 'Market analyst', 'Recruiter', 'Machinist', 'Plant manager', 'Quality control manager']
    it = ['Communications analyst', 'Database administrator', 'E-business specialist', 'Programmer', 'Site manager']
    Sales = ['Branch manager', 'Retail manager', 'Telemarketer']
    dep = 'No Departrment'
    if position in Accounting:
        dep = 'Accounting'
    elif position in Marketing:
        dep = 'Accounting'
    elif position in HumanResources:
        dep = 'Human resources'
    elif position in Production:
        dep = 'Production'
    elif position in it:
        dep = 'IT' 
    elif position in Sales:
        dep = 'Sales'
    return dep

def is_valid_mobile(string):
    mobile_regex = "^09(1[0-9]|3[1-9]|0[1-5])-?[0-9]{3}-?[0-9]{4}$"
    if(re.search(mobile_regex, string)):
        return True
    return False

@login_required(login_url='login')
def accountSettings(request):
	page = 'accountSettings'
	employee = request.user.employee
	form = EmployeeForm(instance=employee)
	mobile = request.POST.get("mobile_number")

	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			if is_valid_mobile(str(mobile)) == False and str(mobile) != "":
				context= {'form': form, 'error':'Your mobile number is not valid' , 'position' : employee.position}
				return render(request, 'base/edit_profile.html', context)
			employee.department = department(employee.position)
			form.save()
			return redirect('view-profile')
	print("-----*****---")
	print(employee.position)
	context = {'form':form, 'page':page , 'position' : employee.position}
	return render(request, 'base/edit_profile.html', context)


class CalendarView(generic.ListView):
    model = In_out
    template_name = 'base/calendar.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        print("------")
        print(d)
        user_id = self.request.user.employee
        cal = Calendar(d.year, d.month)
        in_outs = In_out.objects.all()
        in_out_list = []
        dates_ss = []
        for in_out in in_outs:
            if in_out.employee.id == self.request.user.employee.id:
                in_out_list.append(in_out)
                if str(in_out.start_time.date()) not in dates_ss and in_out.start_time.date().month == d.month:
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
            # t_vals.append(date_time)  
            t_vals.append(date_time.strftime("%H:%M:%S"))  
        chart = get_plot(dates_ss, t_vals)
        html_cal = cal.formatmonth(user_id, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        print("This Part ------------->")
        context['next_month'] = next_month(d)
        context['chart'] = chart
        context['datess'] = dates_ss
        context['timess'] = t_vals
        return context

class IoArchiveReport(generic.ListView):
    model = In_out
    template_name = 'base/io_archive_report.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        username = self.request.GET.get('username', '')
        daterange = self.request.GET.get('daterange', '')
        user_id = 0
        cal = Calendar(d.year, d.month)
        in_outs = In_out.objects.all()
        in_out_list = []
        dates_ss = []
        if daterange!= "":
            (start , end ) = daterange.split("-")
            (sm , sd , sy ) = start.split("/")
            (em , ed  , ey) = end.split("/")
        for in_out in in_outs:
            if in_out.employee.user.username == username:
                user_id = in_out.employee.id
                in_out_list.append(in_out)
                if str(in_out.start_time.date()) not in dates_ss:
                   dates_ss.append(str(in_out.start_time.date()))
        t_vals = []
        for dte in dates_ss:   
            total = []
            for in_out in in_outs:    
                if in_out.employee.user.username == username:
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

        html_cal = cal.formatmonth(user_id, withyear=True , )
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
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
    print(d)
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
	er = False
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
		errors = []
		if passwordvalue1 != passwordvalue2:
			# print("---Password not match")
			# context= {'form': form, 'error':'The passwords that you provided don\'t match'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The passwords that you provided don\'t match')	
			# print("----Password Matched")
		if passwordvalue1 == uservalue:
			# context= {'form': form, 'error':'Your password can’t be too similar to your other personal information. Please try another password.'}
			# print("----Password match username")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password can\'t be too similar to your other personal information. Please try another password.')
		if len(passwordvalue1) < 8:
			# context= {'form': form, 'error':'Your password must contain at least 8 characters. Please try another password.'}
			# print("----Password is too short")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 8 characters. Please try another password.')
		if not re.match('.*[0-9]', passwordvalue1):
			# print("---Your password must contain a number")
			# context= {'form': form, 'error':'Your password must contain a number. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain a number. Please try another password.')
		if not re.match('.*[A-Z]', passwordvalue1):
			# print("---Your password must contain at least 1 upper case character.")
			# context= {'form': form, 'error':'Your password must contain at least 1 upper case character. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 1 upper case character. Please try another password.')
		if not re.match('.*[a-z]', passwordvalue1):
			# print("Your password must contain at least 1 lower case character." )
			# context= {'form': form, 'error':'Your password must contain at least 1 lower case character. Please try another password.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Your password must contain at least 1 lower case character. Please try another password.')			
		try:
			user= User.objects.get(username=uservalue)
			print("User Exist")
			# context= {'form': form, 'error':'The username you entered has already been taken. Please try another username.'}
			# print("----User Exist")
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The username you entered has already been taken. Please try another username.')			
		except User.DoesNotExist:
			print("-----User Not Exist")
		try:
			user= User.objects.get(email=emailvalue)
			# context= {'form': form, 'error':'The email you entered has already been taken. Please try another email.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('The email you entered has already been taken. Please try another email.')			
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
				position = request.POST.get('position')
				department1 = department(position)
				user.groups.add(group)
				Employee.objects.create(
					user = user,
					email = email,
					first_name = first_name,
					last_name = last_name,
					position = position,
					department = department1
				)
				context= {'form': form}
				messages.success(request, 'Account was created for ' + username)
				valid_username = False
				return redirect('employees_list')
		
		if er == False and valid_username and not form.is_valid():
			# print("---Invalid Username")
			# context= {'form': form, 'error':'Please enter a valid username.'}
			# return render(request, 'base/sign-up.html', context)
			er = True
			errors.append('Please enter a valid username.')			

	if er:
		context= {'form': form, 'errors':errors}
		return render(request, 'base/create-user.html', context)

	context = {'form':form}
	return render(request, 'base/create-user.html', context)

    
    
	# valid_username = True
	# emailvalue=''
	# uservalue=''
	# passwordvalue1=''
	# passwordvalue2=''
	# form = CreateUserForm()
	# if request.method == 'POST':
	# 	form = CreateUserForm(request.POST)
	# 	print("Form Created")
	# 	uservalue = request.POST.get('username')
	# 	emailvalue = request.POST.get('email')
	# 	passwordvalue1 = request.POST.get('password1')
	# 	passwordvalue2 = request.POST.get('password2')
	# 	fname = request.POST.get('first_name')
	# 	lname = request.POST.get('last_name')
	# 	if passwordvalue1 == passwordvalue2:
	# 		print("----Password Matched")
	# 		if passwordvalue1 == uservalue:
	# 			context= {'form': form, 'error':'Your password can’t be too similar to your other personal information. Please try another password.'}
	# 			print("----Password match username")
	# 			return render(request, 'base/create-user.html', context)
	# 		if len(passwordvalue1) < 8:
	# 			context= {'form': form, 'error':'Your password must contain at least 8 characters. Please try another password.'}
	# 			print("----Password is too short")
	# 			return render(request, 'base/create-user.html', context)
	# 		if not re.match('.*[0-9]', passwordvalue1):
	# 			print("---Your password must contain a number")
	# 			context= {'form': form, 'error':'Your password must contain a number. Please try another password.'}
	# 			return render(request, 'base/create-user.html', context)
	# 		if not re.match('.*[A-Z]', passwordvalue1):
	# 			print("---Your password must contain at least 1 upper case character.")
	# 			context= {'form': form, 'error':'Your password must contain at least 1 upper case character. Please try another password.'}
	# 			return render(request, 'base/create-user.html', context)
	# 		if not re.match('.*[a-z]', passwordvalue1):
	# 			print("Your password must contain at least 1 lower case character." )
	# 			context= {'form': form, 'error':'Your password must contain at least 1 lower case character. Please try another password.'}
	# 			return render(request, 'base/create-user.html', context)			
	# 		try:
	# 			user= User.objects.get(username=uservalue)
	# 			context= {'form': form, 'error':'The username you entered has already been taken. Please try another username.'}
	# 			print("----User Exist")
	# 			return render(request, 'base/create-user.html', context)
	# 		except User.DoesNotExist:
	# 			print("-----User Not Exist")
	# 			try:
	# 				user= User.objects.get(email=emailvalue)
	# 				context= {'form': form, 'error':'The email you entered has already been taken. Please try another email.'}
	# 				return render(request, 'base/create-user.html', context)
	# 			except:
	# 				print("Email not repeated")
          			
	# 				if form.is_valid():
	# 					print("----Form is Valid")
	# 					user = form.save()
	# 					username = request.POST.get('username')
	# 					email = request.POST.get('email')
	# 					first_name = request.POST.get('first_name')
	# 					last_name = request.POST.get('last_name')
	# 					group = Group.objects.get(name='employee')
	# 					user.groups.add(group)
	# 					Employee.objects.create(
	# 						user = user,
	# 						email = email,
	# 						first_name = first_name,
	# 						last_name = last_name
	# 					)
	# 					context= {'form': form}
	# 					messages.success(request, 'Account was created for ' + username)
	# 					valid_username = False
	# 					return redirect('employees_list')
	# 	else:
	# 		print("---Password not match")
	# 		context= {'form': form, 'error':'The passwords that you provided don\'t match'}
	# 		return render(request, 'base/create-user.html', context)
	# 	if valid_username:
	# 		print("---Invalid Username")
	# 		context= {'form': form, 'error':'Please enter a valid username.'}
	# 		return render(request, 'base/create-user.html', context)
	   
	# context = {'form':form}
	# return render(request, 'base/create-user.html', context)

def editUser(request, pk):
	page = 'editUser'
	employee = Employee.objects.get(id=pk)
	form = EmployeeForm(instance=employee)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES,instance=employee)
		if form.is_valid():
			employee.department = department(employee.position)
			form.save()
			return redirect('employees_list')
	context = {'form':form, 'eid': pk, 'page':page, 'position':employee.position, 'emper':employee}
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

def export_excel(request, fltra, fltrd):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Employees_List ' + \
		str(dtt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Employees')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Firstname', 'Lastname', 'Email' ,'Mobile Number','Department' ,'Position' ,'Status']
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	
	employees = Employee.objects.all()
	employees_list = []
	for employee in employees:
		if employee.user.id != request.user.id:
			if fltra != 'All' and fltrd != 'All':
				if fltra == 'Active':
					if employee.user.is_active and employee.department == fltrd:
						employees_list.append(employee)
				else:
					if not employee.user.is_active and employee.department == fltrd:
						employees_list.append(employee)				
			elif fltra == 'All' and fltrd != 'All':
				if employee.department == fltrd:
					employees_list.append(employee)
			elif fltrd == 'All' and fltra != 'All':
				if fltra == 'Active':
					if employee.user.is_active:
						employees_list.append(employee)
				else:
					if not employee.user.is_active:
						employees_list.append(employee)	
			else:
				employees_list.append(employee)

	for row_num in range(len(employees_list)):
		rowx = row_num+1
		ws.write(rowx, 0, employees_list[row_num].first_name, font_style)
		ws.write(rowx, 1, employees_list[row_num].last_name, font_style)
		ws.write(rowx, 2, employees_list[row_num].email, font_style)
		ws.write(rowx, 3, employees_list[row_num].mobile_number, font_style)
		ws.write(rowx, 4, employees_list[row_num].department, font_style)
		ws.write(rowx, 5, employees_list[row_num].position, font_style)
		ws.write(rowx, 6, 'Active' if employees_list[row_num].user.is_active else 'Inactive', font_style)
	wb.save(response)
	return response

def act_dep_filter(request, fltra, fltrd):
	print("in act_dep_filter")
	print(f"fltra: {fltra}")
	print(f"fltrd: {fltrd}")
	employees = Employee.objects.all()
	employees_list = []
	for employee in employees:
		if employee.user.id != request.user.id:
			if fltra != 'All' and fltrd != 'All':
				if fltra == 'Active':
					if employee.user.is_active and employee.department == fltrd:
						employees_list.append(employee)
				else:
					if not employee.user.is_active and employee.department == fltrd:
						employees_list.append(employee)				
			elif fltra == 'All' and fltrd != 'All':
				if employee.department == fltrd:
					employees_list.append(employee)
			elif fltrd == 'All' and fltra != 'All':
				if fltra == 'Active':
					if employee.user.is_active:
						employees_list.append(employee)
				else:
					if not employee.user.is_active:
						employees_list.append(employee)	
			else:
				employees_list.append(employee)
	context = {'employees' : employees_list, 'fltra' : fltra, 'fltrd' : fltrd}
	return render(request, 'base/employees_list.html', context) 

class ActRep(generic.ListView):
    model = In_out
    template_name = "base/io_archive_report.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        daterange = self.request.GET.get('daterange') if self.request.GET.get('daterange') != None else ''
        if self.request.user.groups.all()[0].name == "admin":  
            sel_user = self.request.GET.get('users') if self.request.GET.get('users') != None else ''
        else:
            sel_user = self.request.user.employee.id
        # s_date = str(datetime.today().strftime('%Y-%m-%d'))
        # e_date = str(datetime.today().strftime('%Y-%m-%d'))
        s_date = ''
        e_date = ''
        if daterange != '':
           s_date =  daterange.split(' - ')[0]
           e_date =  daterange.split(' - ')[1]
        # user_id = self.request.user.employee
        user_id = ''
        employees = Employee.objects.all()
        if sel_user != '':
           for emp in employees:
               if emp.id == int(sel_user):
                  user_id = emp
                  break
           
    
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        in_outs = In_out.objects.all()
        in_out_list = []
        dates_ss = []
        print(f"***{sel_user}")
        for in_out in in_outs:
            if sel_user != '' and in_out.employee.id == int(sel_user):
                in_out_list.append(in_out)
                if str(in_out.start_time.date()) not in dates_ss and in_out.start_time.date().month == d.month:
                   dates_ss.append(str(in_out.start_time.date()))
                   print(in_out.start_time.date().month)
        t_vals = []
        for dte in dates_ss:   
            total = []
            for in_out in in_outs:
                if user_id != '':    
                   if in_out.employee.id == user_id.id:
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
            # t_vals.append(date_time)  
            t_vals.append(date_time.strftime("%H:%M:%S")) 
        
        emps_list = []    
        for emp in employees:
            # if emp.user != self.request.user:
            emps_list.append(emp)
        chart = get_plot(dates_ss, t_vals)
        html_cal = cal.formatmonth_rep(user_id, s_date, e_date ,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['chart'] = chart
        context['datess'] = dates_ss
        context['timess'] = t_vals
        context['employees'] = emps_list
        try:
           context['name'] = str(user_id.id)
        except:
             context['name'] = '' 
        try:
           context['drange'] = daterange
        except:
           context['drange'] = '' 
        return context
    

def export_act_excel(request, name, drange):
	sdate = dtt.datetime.strptime(drange.split(' - ')[0], '%Y-%m-%d').date()
	edate = dtt.datetime.strptime(drange.split(' - ')[1], '%Y-%m-%d').date()
	date_generated = [sdate + dtt.timedelta(days=x) for x in range(0, (edate-sdate).days+1)]
	in_outs = In_out.objects.all()
	in_out_list = []
	dates_ss = []
	for in_out in in_outs:
		if in_out.employee.id == int(name):
			in_out_list.append(in_out)
			if str(in_out.start_time.date()) not in dates_ss:
				dates_ss.append(in_out.start_time.date())
	print(dates_ss)
	t_vals = []
	dh = []
	for dte in dates_ss:   
		total = []
		for in_out in in_outs:
			if in_out.employee.id == int(name):
				if str(in_out.start_time.date()) == str(dte):
					FMT = '%H:%M:%S'
					tdelta = dt.strptime(str(in_out.end_time.time()), FMT) - dt.strptime(str(in_out.start_time.time()), FMT)
					total.append(str(tdelta))
		mysum = dtt.timedelta()
		for i in total:
			(h, m, s) = i.split(':')
			dd = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
			mysum += dd
		if dte not in dh:
			dh.append(dte)
			date_time = dtt.datetime.strptime(str(mysum), "%H:%M:%S")
			# t_vals.append(date_time)  
			t_vals.append(date_time.strftime("%H:%M:%S"))
	print(t_vals)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Activities_Report ' + \
		str(dtt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Employees')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Date', 'Status', 'Working Hours']
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	
	employees = Employee.objects.all()
	employees_list = []
	for employee in employees:
		employees_list.append(employee)
	i = 0
	for row_num in range(len(date_generated)):
		rowx = row_num+1
		ws.write(rowx, 0, str(date_generated[row_num]), font_style)
		if date_generated[row_num] not in dates_ss:
			ws.write(rowx, 1, "Absent", font_style)
			ws.write(rowx, 2, "00:00:00", font_style)

		else:
			ws.write(rowx, 1, "Present", font_style)
			ws.write(rowx, 2, t_vals[i], font_style)
			i += 1
				
	wb.save(response)
	return response


def export_io_excel(request, name, drange):
	sdate = dtt.datetime.strptime(drange.split(' - ')[0], '%Y-%m-%d').date()
	edate = dtt.datetime.strptime(drange.split(' - ')[1], '%Y-%m-%d').date()
	date_generated = [sdate + dtt.timedelta(days=x) for x in range(0, (edate-sdate).days+1)]
	in_outs = In_out.objects.all()
	in_out_list = []
	dates_ss = []
	max_io = 0
	for in_out in in_outs:
		if in_out.employee.id == int(name):
			in_out_list.append(in_out)
			if str(in_out.start_time.date()) not in dates_ss:
				dates_ss.append(in_out.start_time.date())
	print("--------------")
	print(dates_ss)
	t_vals = []
	dh = []
	for dte in dates_ss:   
		total = []
		for in_out in in_outs:
			if in_out.employee.id == int(name):
				if str(in_out.start_time.date()) == str(dte):
					FMT = '%H:%M:%S'
					tdelta = dt.strptime(str(in_out.end_time.time()), FMT) - dt.strptime(str(in_out.start_time.time()), FMT)
					total.append(str(tdelta))
		mysum = dtt.timedelta()
		for i in total:
			(h, m, s) = i.split(':')
			dd = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
			mysum += dd
		if dte not in dh:
			dh.append(dte)
			date_time = dtt.datetime.strptime(str(mysum), "%H:%M:%S")
			# t_vals.append(date_time)  
			t_vals.append(date_time.strftime("%H:%M:%S"))
			max_io += 1
		# else:
	print(t_vals)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=IO_Report ' + \
		str(dtt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Employees')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Date', 'Working Hours']
 
	max_io = 0
	
	employees = Employee.objects.all()
	employees_list = []
	for employee in employees:
		employees_list.append(employee)
	i = 0
	for row_num in range(len(date_generated)):
		rowx = row_num+1
		ws.write(rowx, 0, str(date_generated[row_num]), font_style)
		if date_generated[row_num] not in dates_ss:
			ws.write(rowx, 1, "00:00:00", font_style)

		else:
			ws.write(rowx, 1, t_vals[i], font_style)
			ii = 0
			for io in in_out_list:
				print(io.start_time.date())
				if str(io.start_time.date()) == str(dates_ss[i]):
					ws.write(rowx, 2 + 2*ii, str(io.start_time.time()), font_style)
					ws.write(rowx, 3 + 2*ii, str(io.end_time.time()), font_style)
					max_io += 1
					ii += 1
			i += 1
   
	for i in range(1, max_io):
		columns.append(f"Entry {i}")
		columns.append(f"Exit {i}")
		print(columns)
 
	for col_num in range(len(columns)):
		ws.write(0, col_num, columns[col_num], font_style)
	
	wb.save(response)
	return response

def dep_filter(request, dep, drange):
	print(dep)
	print(drange)
	employees = Employee.objects.all()
	employees_list = []
	if dep != 'All':
		for emp in employees:
			if emp.department == dep:
				employees_list.append(emp)
	else:
		for emp in employees:
			employees_list.append(emp)
   

	s_date =  drange.split(' - ')[0]
	e_date =  drange.split(' - ')[1]
	in_outs = In_out.objects.filter(start_time__range=[dtt.datetime.strptime(s_date, "%Y-%m-%d"), dtt.datetime.strptime(e_date, "%Y-%m-%d")])
	print("---------------")
	for io in in_outs:
		print(io.employee.first_name + "----" + str(io.start_time) + "----" + str(io.end_time))
	print("----------------")

	print(employees_list)
    
	working_hours = []
	names = []
	for emp in employees_list:
		in_out_nums = 0
		for in_out in in_outs:
			if in_out.employee.id == emp.id:
				in_out_nums += 1
		if in_out_nums > 0:
			in_out_list = []
			for in_out in in_outs:
				if in_out.employee.id == emp.id:
					in_out_list.append(in_out)
			if len(in_out_list) > 0:
				timeList = []
				timeList1 = []
				for ins in in_out_list:
					timeList.append(str(ins.start_time.time()))
					timeList1.append(str(ins.end_time.time()))

				mysum1 = dtt.timedelta()
				for i in timeList:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum1 += d
				print(str(mysum1))
				mysum2 = dtt.timedelta()
				for i in timeList1:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum2 += d
					
				print(str(mysum2))

				time = mysum2 - mysum1
				print("----------------")
				print(time)
				print("----------------")
				working_hours.append(time)

 
			names.append(emp.id)
		else:
			working_hours.append("00:00:00")
   


	emps_list = zip(employees_list, working_hours)
 
	return render(request, 'base/io_report.html', {'employees': emps_list, 'dep':dep, 'drange' : drange})


def export_total_hours(request, dep, drange):
	sdate = dtt.datetime.strptime(drange.split(' - ')[0], '%Y-%m-%d').date()
	edate = dtt.datetime.strptime(drange.split(' - ')[1], '%Y-%m-%d').date()
	date_generated = [sdate + dtt.timedelta(days=x) for x in range(0, (edate-sdate).days+1)]
	s_date =  drange.split(' - ')[0]
	e_date =  drange.split(' - ')[1]
	employees = Employee.objects.all()
	employees_list = []
	if dep != 'All':
		for em in employees:
			if em.department == dep:
				employees_list.append(em)
	else:
		for em in employees:
			employees_list.append(em)
	in_outs = In_out.objects.filter(start_time__range=[dtt.datetime.strptime(s_date, "%Y-%m-%d"), dtt.datetime.strptime(e_date, "%Y-%m-%d")])
	print("---------------")
	for io in in_outs:
		print(io.employee.first_name + "----" + str(io.start_time) + "----" + str(io.end_time))
	print("----------------")
	dates_ss = []
	for in_out in in_outs:
		if in_out.employee.department == dep:
			if str(in_out.start_time.date()) not in dates_ss:
				dates_ss.append(in_out.start_time.date())
	print("******")
	print(dates_ss)
	working_hours = []
	for emp in employees_list:
		in_out_list = []
		in_out_nums = 0
		for in_out in in_outs:
			if in_out.employee.id == emp.id:
				in_out_nums += 1
		if in_out_nums > 0:
			for in_out in in_outs:
				if in_out.employee.id == emp.id:
					in_out_list.append(in_out)
			if len(in_out_list) > 0:
				timeList = []
				timeList1 = []
				for ins in in_out_list:
					timeList.append(str(ins.start_time.time()))
					timeList1.append(str(ins.end_time.time()))

				mysum1 = dtt.timedelta()
				for i in timeList:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum1 += d
				print(str(mysum1))
				mysum2 = dtt.timedelta()
				for i in timeList1:
					(h, m, s) = i.split(':')
					d = dtt.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
					mysum2 += d
					
				print(str(mysum2))

				time = mysum2 - mysum1
				print("----------------")
				print(time)
				print("----------------")
				working_hours.append(str(time))
		else:
			working_hours.append("00:00:00")

	print(working_hours)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Activities_Report ' + \
		str(dtt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Working Hours')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	columns = ['Name', 'Working Hours']
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	
	 
	for rowx in range(len(employees_list)):
		ws.write(rowx+1, 0, employees_list[rowx].first_name + " " + employees_list[rowx].last_name, font_style)
		ws.write(rowx+1, 1, working_hours[rowx], font_style)
					
	wb.save(response)
	return response

def add_position(request):

	form = CreatePositionForm()
	if request.method == 'POST':
		form = CreatePositionForm(request.POST)
		print("Form Created")
		if form.is_valid():
			print("----Form is Valid")
			name = request.POST.get('name')
			department = request.POST.get('department')
			Position.objects.create(
				name = name,
				department = department
			)
			return redirect('employees_list')


	context = {'form':form}
	return render(request, 'base/create-position.html', context)

def switch_role(request, pk):
    print("-------****---------")
    emp = Employee.objects.get(id=pk)
    print(emp.user.id)
    user = User.objects.get(id=emp.user.id)
    print(user.groups.all()[0].name)
    if user.groups.all()[0].name == "employee":
       print("-------****---------")
       group = Group.objects.get(name='admin')
       user.groups.add(group)
       group = Group.objects.get(name='employee')
       user.groups.remove(group)
    else:
       print("-------FK---------")
       group = Group.objects.get(name='employee')
       user.groups.add(group)
       group = Group.objects.get(name='admin')
       user.groups.remove(group)
    print("-------****---------")
    return redirect('edit-user', pk)

    
    

