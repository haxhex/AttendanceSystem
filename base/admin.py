from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from base.models import Event
from .models import *

# Register your models here.

# class AccountInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = 'Accounts'
    
# class CustomizeUserAdmin (UserAdmin):
#     inlines = (AccountInline, )
    
# admin.site.unregister(User)
# admin.site.register(User, CustomizeUserAdmin)
admin.site.register(Employee)
admin.site.register(In_out)
admin.site.register(Event)
admin.site.register(Position)



