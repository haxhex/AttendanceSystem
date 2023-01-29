from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path("", views.home, name="home"),
    path("", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path("dashboard/", login_required(views.CalendarView.as_view()), name="dashboard"),
    path("io/", views.io, name="io"),
    path("io-archive/", views.login_required(views.ActRep.as_view()), name="io-archive"),
    path("io-report/", views.io_report, name="io-report"),
    path("face/" , views.face , name = "face"),
    path("io-archive-report/", login_required(views.ActRep.as_view()), name="io-archive-report"),
    path("view-profile/", views.view_profile, name="view-profile"),
    path("edit-profile/", login_required(views.accountSettings), name="edit-profile"),
    path("password-change/" , views.password_change , name="password-change" ),
    path("password_reset/", views.password_reset_request, name="password_reset"), 
    path("employees_list/", views.employees_list, name="employees_list"), 
    path("create-user/", views.createUser, name="create-user"), 
    path('edit-user/<str:pk>/', views.editUser, name="edit-user"), 
    path("change-pass/<str:pk>/" , views.changeUserPass , name="change-pass"), 
    path("delete-user/<str:pk>/" , views.deleteUser , name="delete-user"), 
    path("change-status/<str:pk>/" , views.change_status , name="change-status"), 
    path("export-excel/<str:fltra>/<str:fltrd>/" , views.export_excel , name="export-excel"),
    path("act-dep-filter/<str:fltra>/<str:fltrd>/" , views.act_dep_filter , name="act-dep-filter"),  
    path('export-act-excel/<str:name>/<str:drange>/', views.export_act_excel, name="export-act-excel"),
    path('export-io-excel/<str:name>/<str:drange>/', views.export_io_excel, name="export-io-excel"),
    path('export-total-hours/<str:dep>/<str:drange>/', views.export_total_hours, name="export-total-hours"),
    path('add-position/', views.add_position, name="add-position"),
    path('switch-role/<str:pk>/', views.switch_role, name="switch-role"),
    # path('register-face/', views.register_face, name="register-face"),
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
	re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path("dep-filter/<str:dep>/<str:drange>/", views.dep_filter, name="dep-filter"), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

