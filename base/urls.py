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
    path("view-profile/", views.view_profile, name="view-profile"),
    path("edit-profile/<str:pk>/", views.edit_profile, name="edit-profile"),
    path("password-change/" , views.password_change , name="password-change" )
        
]
