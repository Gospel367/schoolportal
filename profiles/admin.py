from django.contrib import admin

from . models import ClassForm, PostComments, Posts, Apply,  Logo,  CustomUser, ClassForm, Exam, StudentComplain, TeacherComplain, HOD,  Staffdata, Student_field, Allcourses, Payment_info, Level, Departments #, RegisterCourses
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username',  'email', 'first_name', 'last_name', 'is_staff', 'is_student', 'is_teacher', 'mailing_address', 'phone', 'state', 'country')
    search_fields =['username', 'status']

    
    fieldsets = ( 
                 ( None, { 'fields': ('username', 'password') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),

                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student', 'is_teacher', 'mailing_address',  'phone', 'state', 'country', 'profile_pic', 'study_field', 'class_enrolled')}),
                 
                 )
    
    add_fieldsets = ( 
                 ( None, { 'fields': ('username', 'password1', 'password2') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
                 
                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student', 'is_teacher', 'mailing_address', 'phone', 'state', 'country', 'profile_pic', 'study_field', 'class_enrolled')}),
                 
                 )
  
class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ['heading', 'body', 'active', 'email'] 
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        
  
class TeacherComplainAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'subject', 'description', 'resolved']
    
    
    
class StudentComplainAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'subject', 'description', 'resolved']
    
    
    
class PostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_date', 'author', 'slug']
    prepopulated_fields = {'slug': ('title',)}   
     
     
     
class ClassFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 
  
    

class HODAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'slug']
    prepopulated_fields = {'slug': ('full_name',)}   
    
    
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ['dept_name', 'hod', 'slug']
    prepopulated_fields = {'slug': ('dept_name',)}


class LogoAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'slug']
    prepopulated_fields = {'slug': ("slug",)}


class LevelAdmin(admin.ModelAdmin):
    list_display = ['class_name',  'slug']
    prepopulated_fields = {'slug': ('class_name',)}
    

class StaffdataAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'email', 'phone', 'dept']
    prepopulated_fields = {'slug': ('nickname',)}
    
    
class Student_fieldAdmin(admin.ModelAdmin):
    list_display = ['field_title', 'slug']
    prepopulated_fields = {'slug': ('field_title',)}
    
    
class AllcoursesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'field']
    prepopulated_fields = {'slug': ('title',)}
    
   
class Payment_infoAdmin(admin.ModelAdmin):
    list_display = ['paid', ]


class ExamAdmin(admin.ModelAdmin):
    list_display =[ 'student_username', 'course',  'scores']
    #prepopulated_fields = {'slug': ('slug',)}
 
 
class ApplyAdmin(admin.ModelAdmin):
     list_display = ['firstname', 'lastname', 'phone', 'class_choice']
     prepopulated_fields = {'slug': ('firstname',)}
     
class RegistercoursesAdmin(admin.ModelAdmin):
     list_display = ['student_username',]
     prepopulated_fields = {'slug': ('course',)}



admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(RegisterCourses, RegistercoursesAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Staffdata, StaffdataAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Student_field, Student_fieldAdmin)
admin.site.register(Allcourses, AllcoursesAdmin)
admin.site.register(ClassForm, ClassFormAdmin)
admin.site.register(HOD, HODAdmin)
admin.site.register(Payment_info, Payment_infoAdmin)
admin.site.register(TeacherComplain, TeacherComplainAdmin)
admin.site.register(StudentComplain, StudentComplainAdmin)
admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(Logo, LogoAdmin)
admin.site.register(Posts, PostsAdmin)



