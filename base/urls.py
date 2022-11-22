from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("io/", views.io, name="io"),
    path("io-archive/", views.io_archive, name="io-archive"),
    path("io-report/", views.io_report, name="io-report"),
    path("io-archive-report/", views.io_archive_report, name="io-archive-report"),
    path("view-profile/", views.view_profile, name="view-profile"),
    path("edit-profile/", views.accountSettings, name="edit-profile"),
    path("password-change/" , views.password_change , name="password-change" ),
    path("password_reset/", views.password_reset_request, name="password_reset"), 
    path("employees_list/", views.employees_list, name="employees_list"),  
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
	re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]
