import string
from django.utils.crypto import get_random_string
import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

SCHOOL_YEAR =(
    ( 1 , '2019/20' ),
    (2 , '2020/21'),
    (3 , '2021/22'),
)

paytype =(
    ( 1 , '60%' ),
    (2 , '100%'),
)

def validate_pass(value):
    if len(str((value) ))< 6:
        raise ValidationError(
            _('%(value)s is not up to 7 digits'),
                              params={'value': value},
        )



def unique_slugify(instance, slug):
    model=instance.__class__
    unique_slug=slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug=slug+get_random_string(length=4)
    return unique_slug

    
    
TITLE_CHOICE = (
    (1,  'Mr.'), 
    (2,  'Mrs.'), 
    (3,  'Engr.'), 
    (4,  'Prof.'), 
    (5,  'Ms.')
)

STATUS_CHOICE = (
    (1,  'student'), 
    (2,  'teacher')
)

class Student_field(models.Model):
    field_title = models.CharField(max_length=200,  null=True,  blank=True)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['field_title']
        verbose_name = 'Student Field'
        verbose_name_plural = 'Student Fields'

    def __str__(self):
        return self.field_title

    def save(self,  *args,  **kwargs):
        self.slug = slugify(self.field_title)
        super(Student_field,  self).save(*args,  **kwargs)
        
        
        
class ClassForm(models.Model):
    name = models.CharField(max_length=200,  null=True)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'

    def __str__(self):
        return self.name

       
class Level(models.Model):
    class_name = models.CharField(max_length=200,  null=True)
    classform = models.ForeignKey(ClassForm, on_delete=models.CASCADE, blank=True, null=True, related_name='classform')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['class_name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.class_name


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to ='media/', null = True, blank =True)
    phone = models.IntegerField( unique=True, null= True, blank = True, validators=[validate_pass])
    country = models.CharField(max_length=200,  null = True, blank=True)
    state = models.CharField(max_length=200,  null = True, blank=True)
    is_student = models.BooleanField(default=0)
    is_teacher = models.BooleanField(default=0)
    mailing_address = models.CharField(max_length=200, null = True,   blank=True)
    study_field = models.ForeignKey(Student_field, on_delete=models.CASCADE, blank=True, null=True)
    class_enrolled = models.ForeignKey(Level, on_delete=models.CASCADE,  blank=True, null=True, related_name='studentlevel')
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    
class Allcourses(models.Model):
    title = models.CharField(max_length=200,  null=True,  blank=True)
    field = models.ForeignKey(Student_field,  on_delete=models.CASCADE,  blank=True, null=True, related_name='field_course')
    teacher_in_charge = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, blank=True, null=True, related_name='course_teacher')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def save(self,  *args,  **kwargs):
        self.slug = slugify(self.title)
        super(Allcourses,  self).save(*args,  **kwargs)
        

class HOD(models.Model):
    title = models.IntegerField(choices=TITLE_CHOICE,  default=0)
    full_name = models.CharField(max_length=200,  null=True)
    slug = models.SlugField(max_length=200,  null=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Head of Department'
        verbose_name_plural = 'Head of Departments'

    def __str__(self):
        return self.full_name


class Departments(models.Model):
    dept_name = models.CharField(max_length=200,  null=True)
    hod = models.ForeignKey(HOD,  on_delete=models.CASCADE)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['dept_name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.dept_name



class Staffdata(models.Model):
    nickname = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200,  null=True,  blank=True)
    lastname = models.CharField(max_length=200,  null=True,  blank=True)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    staff_image = models.ImageField(upload_to='media/', null=True)
    state = models.CharField(max_length=200,  )
    dept = models.ForeignKey(Departments,  on_delete=models.CASCADE, related_name='deptstaff')
    date_employed = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['nickname']
        verbose_name = 'staffdatum'
        verbose_name_plural = 'staffdata'

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def save(self,  *args,  **kwargs):
        self.slug = slugify(self.nickname)
        super(Staffdata,  self).save(*args,  **kwargs)


class Logo(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='media/')
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def __str__(self):
        return self.name
    
    def save(self,  *args,  **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args,  **kwargs)

    
    
class Payment_info(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='studentfees', null=True, blank=True)
    session = models.IntegerField(choices=SCHOOL_YEAR, default=1)
    percentage = models.IntegerField(choices=paytype, default=1)
    paid = models.BooleanField(default=0)
    
    class Meta:
        ordering = ['paid']

    def __str__(self):
        return self.student.first_name



class Exam(models.Model):
    student_username = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='registercourseuser')
    course = models.ForeignKey(Allcourses, blank=True, on_delete=models.CASCADE, null = True, related_name='registercoursename')
    scores =models.FloatField(default =0,blank=True, null =True)
    total_score =models.FloatField(default =0, blank=True, null =True)
    cum_score =models.FloatField(default =0, blank=True, null =True)
    grade =models.CharField( max_length=5,  blank=True, null =True)
    slug =models.SlugField( max_length=50, unique=True,  null=True, blank=True)
   
   
    def __str__(self):
        return self.student_username.username
    
    def save(self,  *args,  **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.student_username))
        super().save(*args,  **kwargs)
        
    def save(self,  *args,  **kwargs):
        self.total_score = self.cum_score +(self.scores)
        #if self.total_score
        super().save(*args,  **kwargs)



class Apply(models.Model):
    nickname = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name ='applicants')
    firstname = models.CharField(max_length=200, null=True, blank=True)
    middlename = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to ='media/', null = True, blank =True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateTimeField()
    nationality = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    class_choice = models.ForeignKey(Level, on_delete=models.CASCADE)
    is_admitted =models.BooleanField(default=False)
    slug = models.SlugField(max_length=10, null=True)

    class Meta:
        ordering = ['firstname']
        verbose_name = 'Admission Application'
        verbose_name_plural = 'Admission Applications'
        
    def __str__(self):
        return 'Admission application of {} {} {} for class of {}'.format(self.firstname, self.middlename, self.lastname, self.firstname, self.class_choice.class_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.firstname)
        super(Apply, self).save(*args, **kwargs)
        
class Posts(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug =models.SlugField(max_length=100)
    author =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/')
    
    class Meta:
        ordering = ['post_date']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Posts, self).save(*args, **kwargs)
        
        
class TeacherComplain (models.Model):
    nickname = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teachername')  
    fullname = models.CharField(max_length=100,  null=True, blank=True)  
    subject = models.CharField(max_length=100, null=True, blank=True, default='Heading for complaint')
    description = models.TextField(max_length=2000, null=True, blank=True, default='Describe your complaint here')
    recommendation = models.TextField(max_length=2000, null=True, blank=True, default='Tell us what you think is the solution to this issue? If you have no idea, leave it blank')
    resolved = models.BooleanField(default=False)
    
    
class StudentComplain (models.Model):
    nickname = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    fullname = models.CharField(max_length=100,  null=True, blank=True)  
    subject = models.CharField(max_length=100, null=True, blank=True, default='Heading for complaint')
    description = models.TextField(max_length=2000, null=True, blank=True, default='Describe your complaint here')
    recommendation = models.TextField(max_length=2000, null=True, blank=True, default='Tell us what you think is the solution to this issue? If you have no idea, leave it blank')
    resolved = models.BooleanField(default=False)

class Attendance(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class PostComments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments', null=True)
    name =models.CharField(max_length=200, null=True, blank=True)
    email =models.EmailField(max_length=100)
    heading =models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(null =True, auto_now_add=True)
    body =models.TextField()
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.heading
