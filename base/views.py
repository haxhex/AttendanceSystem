from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'base/home.html')

def loginPage(request):
    if request.user.is_authenticated:
        return render(request ,'base/dashboard.html')
   
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
            return render(request ,'base/dashboard.html')
        else:
            messages.error(request, 'Username or Password does not exist')
            
    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    return render(request ,'base/dashboard.html')
    
