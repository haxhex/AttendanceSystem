from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth. forms import UserCreationForm



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
    return render(request ,'base/dashboard.html')

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
    
