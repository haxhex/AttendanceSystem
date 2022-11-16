from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth. forms import UserCreationForm
from .forms import *
from django.http import HttpResponse
from .models import *
from .forms import SetPasswordForm




def home(request):
    return render(request, 'base/home.html')

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('dashboard')
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page' : page}        
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    in_outs = In_out.objects.all()
    context = {'in_outs' : in_outs}
    return render(request ,'base/dashboard.html', context)

def io(request):
    return render(request ,'base/io.html')

def io_archive(request):
    return render(request ,'base/io_archive.html')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()    
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'An error occcured during registeration')   
    return render(request, 'base/login_register.html', {'form' : form})

def view_profile(request):
    return render(request, 'base/view_profile.html')

def edit_profile(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('view-profile')
        
    context = {'form' : form}
    return render(request, 'base/edit_profile.html', context)

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