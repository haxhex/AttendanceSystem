from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("io/", views.io, name="io"),
    path("io-archive/", views.io_archive, name="io-archive"),
    
]
