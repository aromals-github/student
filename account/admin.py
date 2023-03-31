
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class AccountsAdmin(UserAdmin):
    
    list_display        = ('username','email','is_admin','id','is_superuser')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id',)
    
    filter_horizontal   = ()
    list_filter         = ('is_admin',)
    fieldsets           = ()
admin.site.register(Accounts,AccountsAdmin)


@admin.register(Student_Info)
class Student_Information(admin.ModelAdmin):
    list_display = ("id","name")
    
@admin.register(Approval)
class Student_Approval(admin.ModelAdmin):
    list_display = ("student",'status')