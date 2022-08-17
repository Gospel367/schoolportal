from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from studentportal.models import CustomUser2


class CustomUser2Admin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_teacher', 'is_student', 'mailing_address', 'phone', 'state', 'country')
    
    fieldsets = ( 
                 ( None, { 'fields': ('username', 'password') }),
                 ('Personal info', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
                 ('important dates', {'fields': ('last_login', 'date_joined') }),
                 ('Additional info:', {'fields': ( 'mailing_address', 'phone', 'state', 'country')}),
                 
                 )
    
    add_fieldsets = ( 
                 ( None, { 'fields': ('username', 'password1', 'password2') }),
                 ('Personal info', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
                 ('important dates', {'fields': ('last_login', 'date_joined') }),
                 ('Additional info:', {'fields': ('mailing_address',  'phone', 'state', 'country')}),
                 
                 )

admin.site.register(CustomUser2, CustomUser2Admin)
