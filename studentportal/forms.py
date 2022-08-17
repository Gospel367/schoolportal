from profiles.models import Allcourses, Apply, CustomUser, Staffdata, Exam
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_pass(value):
    if len(str((value) ))< 6:
        raise ValidationError(
            _('%(value)s is not up to 7 digits'),
                              params={'value': value},
        )


class Staffproform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'        
        exclude =['username', 'slug', 'first_name', 'date_joined', 'class_enrolled', 'password', 'study_field', 'classhandled', 'courses_handled', 
                  'last_name',  'country','state', 'last_login', 'groups', 'user_permissions', 'is_staff', 'is_superuser',  'is_teacher', 'is_active', 'is_student'
                  ]
        

class Applyform(forms.ModelForm):
    class Meta:
        model = Apply
        fields = '__all__'  
        exclude = ['nickname', 'slug', 'is_admitted']      
        

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'state', 'phone', 'country', 'mailing_address']


class Examform(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'student_username', 'cum_score', 'scores']
        
        
class TeachersForm(forms.ModelForm):
    class Meta:
        model = Allcourses
        fields = '__all__'