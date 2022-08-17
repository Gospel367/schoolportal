import csv
from datetime import timezone
from django.forms import SlugField
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, UpdateView, FormView, ListView, View, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView
#from numpy import unique
from profiles.models import  Level, Payment_info, Staffdata, CustomUser, Apply, Exam, Logo, Student_field, Staffdata as StaffdataModel, Allcourses,  StudentComplain, TeacherComplain
from profiles.views import Staffs
import studentportal
from .forms import  Applyform, Examform, RegisterForm, Staffproform, TeachersForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
#from .render import Render
from django.db.models import Avg
from studentportal.token import account_activation_token

'''from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail'''

class PasswordReset(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name ='password_reset_email.html'
    subject_template_name ='password_reset_subject.txt'
    extra_email_context = None

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    
    
class PasswordResetComplete(PasswordResetDoneView):
    template_name = 'password_reset_complete.html'


class AdmissionStat(LoginRequiredMixin, ListView):
    model = Apply
    template_name ='admissionstat.html'
    context_object_name ='applicantlist'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = context['applicantlist'].filter(nickname=self.request.user)
        context['logo'] = Logo.objects.all()

        return context
    

class Applicantlist(LoginRequiredMixin, ListView):
    model = Apply
    template_name ='allapplicants.html'
    context_object_name ='applicantlist'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['admitted'] = Apply.objects.filter(is_admitted = True)
        context['unadmitted'] = Apply.objects.filter(is_admitted = False)
        context['approved'] = Apply.objects.filter(nickname__is_student=True)

        return context
    
class ApplicantlistDetail(LoginRequiredMixin, DetailView):
    model = Apply
    template_name ='allapplicantsdetail.html'
    context_object_name ='applicantsdetail'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()

        return context    

class Updateapplication(LoginRequiredMixin, CreateView):
    model = Apply
    template_name ='application.html'
    fields = '__all__'
    
    def get_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        
        return context
    
def get_success_url(self):
        return reverse_lazy('applicantlist')    


    
class PortalRegister(FormView):
    form_class = RegisterForm
    template_name = 'portalregister.html'
    redirect_authenticated_user = True
    
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            user =form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active =False
            user.save()
            
            current_site = get_current_site(request)
            subject ='Activate Your Account'
            message =render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please ' + user.username + ' Confirm your email to complete registration'))
            return redirect('register')
        return render(request, self.template_name, {'form':form})
  
    
'''class PortalRegister(FormView):
    form_class = Register
    template_name = 'portalregister.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('portal')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(
            form.cleaned_data["password"]
        )
        user=form.save(commit=True)
        if user is not None:
            login(self.request, user)
        return super(PortalRegister, self).form_valid(form)'''


class CustomLoginView(LoginView):
    template_name = 'portallogin.html'
    fields = '__all__'
    redirect_authenticated_user = True


class CustomLogout(LogoutView):
    pass




class Updatestudentdata(LoginRequiredMixin,  UpdateView):
    model = CustomUser
    template_name = 'createstudentdata.html'
    fields = [ 'first_name', 'last_name', 'email', 'phone', 'country','state', 'study_field', 'class_enrolled']

    def form_valid(self, form):
        user = form.save(commit=False)
        return super(Updatestudentdata, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()

        return context

    def get_success_url(self):
        return reverse_lazy('studentprofile')


class Portal(ListView):
    model = Student_field
    template_name = 'portal.html'
    context_object_name = 'studentfields'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()

        return context


class Staffdata(LoginRequiredMixin, ListView):
    model = CustomUser
    form_class = Staffproform
    template_name = 'staffdata.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users1'] = context['users'].filter(username=self.request.user)
        context['userinfo2'] = self.request.user
        context['mycourses'] = Allcourses.objects.filter(teacher_in_charge =self.request.user)
        context['logo'] = Logo.objects.all()

        return context
    
class ApplicationForm(LoginRequiredMixin, FormView):
    model = Apply
    form_class = Applyform
    template_name = 'application.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('admissionstat') 
    
    def form_valid(self, form):
        form.instance.nickname = self.request.user
        return super(ApplicationForm, self).form_valid(form)

   
    def get(self, *args, **kwargs):          
        if self.model.objects.filter(nickname=self.request.user).exists():
            return redirect('admissionstat')
        else:
            return super(ApplicationForm, self).get(*args, **kwargs)   
 
    def form_valid(self, form):
        form.instance.nickname = self.request.user
        self.request.user = form.save()
        if self.request.user is not None:
            self.request.user = form.save(commit=False)
        return super(ApplicationForm, self).form_valid(form)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        
        return context
 
class Updateapplication(LoginRequiredMixin, UpdateView):
    model = Apply
    template_name ='application.html'
    fields = '__all__'
    
    def get_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        
        return context
    
    def get_success_url(self):
        return reverse_lazy('applicantlist')         

class Createstaffdata(LoginRequiredMixin,  FormView):
    model = CustomUser
    form_class = Staffproform
    template_name = 'createstaffdata.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('staffprofile') 


    def get(self, *args, **kwargs):          
        if self.model.objects.get(username=self.request.user).exists():
            return redirect('staffprofile')
        else:
            return super(Createstaffdata, self).get(*args, **kwargs)   
 
    def form_valid(self, form):
        form.instance.nickname = self.request.user
        self.request.user = form.save(commit=True)
        return super(Createstaffdata, self).form_valid(form)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        
        return context
    

class Updatestaffdata(LoginRequiredMixin,  UpdateView):
    model = CustomUser
    form_class = Staffproform
    template_name = 'createstaffdata.html'
    context_object_name ='staffdata'

    def form_valid(self, form):
        form.instance.nickname = self.request.user
        return super(Updatestaffdata, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()

        return context

    def get_success_url(self):
        return reverse_lazy('staffprofile')


class Studentprofile(LoginRequiredMixin,  ListView):
    model = Apply  
    template_name = 'studentdata.html'
    context_object_name = 'studentprofile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userdata2'] = context['studentprofile'].filter(nickname=self.request.user)
        context['logo'] = Logo.objects.all()
        context['studentexams'] = Exam.objects.filter(student_username =self.request.user)

        return context



class Staffdashboard(LoginRequiredMixin,  View):
    def get(self, request):
        return render(request, 'staffdashboard.html')

    '''def get(self, request):
        if request.user.is_teacher or request.user.is_superuser:
            return render(request, 'staffdashboard.html')
        return render('register')'''


class Studentdashboard(View):
    def get(self, request):
        return render(request, 'studentdashboard.html')


class ExamView(DetailView):
    model =Exam
    context_object_name ='studentscore'
    template_name = 'studentscore.html'
    

class CreateExam(LoginRequiredMixin, FormView):
    model = Exam
    form_class = Examform
    template_name = 'newscores.html'
    
    def get_success_url(self):
        return reverse_lazy('newexamscores') 
    
    def form_valid(self, form):
        
        form.instance.teacher_username = self.request.user
        self.request.user = form.save(commit =True)
        return super(CreateExam, self).form_valid(form)
   
    '''def form_valid(self, form):
        if self.request.user is None:
            self.request.user = form.save(commit=False)
        else:
            self.request.user = form.save(commit=True)
        return super(CreateExam, self).form_valid(form)'''
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['mycourses'] = Allcourses.objects.filter(teacher_in_charge =self.request.user)
        return context       

class UpdateExam(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = Examform
    template_name = 'updatescore.html'
    success_message ='Scores  saved. Go back to previous '

    def get_success_url(self):
        return reverse_lazy('comptest', kwargs={'pk':self.object.student_username.class_enrolled.pk})
    
    
    def form_valid(self, form):
        if form.instance.total_score >=75:
            form.instance.grade ='A'
        elif form.instance.total_score >65<= 74:
            form.instance.grade ='AB'
        elif form.instance.total_score >60<= 65:
            form.instance.grade ='B'
        elif form.instance.total_score >50<= 60:
            form.instance.grade ='BC'
        elif form.instance.total_score >40<= 50:
            form.instance.grade ='C'
        elif form.instance.total_score >30<= 40:
            form.instance.grade ='D'
        elif form.instance.total_score <= 30:
            form.instance.grade ='F'
        
        form.instance.teacher_username = self.request.user
        self.request.user = form.save(commit =True)
        return super(UpdateExam, self).form_valid(form)
   
    '''def form_valid(self, form):
        if self.request.user is None:
            self.request.user = form.save(commit=False)
        else:
            self.request.user = form.save(commit=True)
        return super(CreateExam, self).form_valid(form)'''
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['return'] = self.object.student_username.class_enrolled

        return context       
        
    
class Viewscores(LoginRequiredMixin,  ListView): 
    model = Exam
    template_name = 'viewscores.html' 
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['courseregs'] = Exam.objects.filter(student_username =self.request.user)
            context['totalcount'] = Exam.objects.filter(student_username =self.request.user).count()
            context['avgscore'] = Exam.objects.filter(student_username =self.request.user).aggregate(Avg('total_score'))
            context['passed_courses'] = Exam.objects.filter(student_username=self.request.user).filter(total_score__gte=49).count()
            context['failed_courses'] = Exam.objects.filter(student_username=self.request.user).filter(total_score__lte= 50).count()

            return context          


class TeacherNewComplaints(LoginRequiredMixin, CreateView):
    model = TeacherComplain
    template_name ='complaints.html'
    fields =['subject', 'description', 'recommendation']
    context_object_name ='teachercomplains'
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            #context['mycomplains'] = context['teachercomplains'].filter(nickname=self.request.user)
            context['logo'] = Logo.objects.all()
            context['mycomplains'] = TeacherComplain.objects.filter(nickname=self.request.user)

            return context       
    
    def form_valid(self, form):
        form.instance.nickname = self.request.user 
        form.instance.fullname = '{} {}'.format(self.request.user.first_name, self.request.user.last_name) 
        self.request.user = form.save(commit =True)
        return super(TeacherNewComplaints, self).form_valid(form)

    
    def get_success_url(self):
        return reverse_lazy('complaints') 
    
         
class StudentNewComplaints(LoginRequiredMixin, CreateView):
    model = StudentComplain
    template_name ='complaints copy.html'
    fields =['subject', 'description', 'recommendation']
    context_object_name ='studentcomplains'
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['mycomplains'] = StudentComplain.objects.filter(nickname=self.request.user)
            return context       
    
    def form_valid(self, form):
        form.instance.nickname = self.request.user 
        form.instance.fullname = '{} {}'.format(self.request.user.first_name, self.request.user.last_name) 
        self.request.user = form.save(commit =True)
        return super(StudentNewComplaints, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('studentcomplaints') 
         

def Studclasses(request, pk):
    pyt = CustomUser.objects.filter(is_student=1).filter(class_enrolled=5)
    context = {
        'pyt': pyt
    }
    return render(request, 'studclasses.html', context )    


def Studentclasses(request, pk):
    #similar posts starts here
    pub = Teachers.objects.filter(slug=pk)
    '''for jon in pub1.classhandled.all():
        bon = jon
    pub =pub1.examteach.all()'''
    context = {
        'pub': pub,
        }
    return render(request, 'studentclasses.html', context)


def Studentclasses2(request, pk):
    #similar posts starts here
    pub1 = Level.objects.get(slug=pk)
    '''pub =pub1.examteach.all()

    for jon in pub1.classhandled.all():
        bon = jon ''' 
    pub =pub1.studentclass.all()
    context = {
        'pub': pub,
        }
    return render(request, 'studentclasses copy.html', context)

    
class RegisterCourses(LoginRequiredMixin, CreateView):
    model = Exam
    template_name ='coursereg.html'
    fields =[ 'course']  
    context_object_name ='coursereg'
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['courseregs'] = Exam.objects.filter(student_username=self.request.user)
           # context['teacherlist'] = CustomUser.objects.filter(is_teacher= 1)
            context['teacherlist'] = Allcourses.objects.all()
            return context       
    
    
    def form_valid(self, form):
        form.instance.student_username = self.request.user
   
        form.instance.studclass = self.request.user.class_enrolled
        self.request.user = form.save(commit =True)
        return super(RegisterCourses, self).form_valid(form)
    
    
    
    def get_success_url(self):
        return reverse_lazy('coursereg')
    
    
class PaymentStatus(LoginRequiredMixin, CreateView):
    model = Payment_info
    template_name ='payment.html'
    fields =['session', 'percentage'] 
    context_object_name ='payment'
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['teacherlist'] = Allcourses.objects.all()
            
            return context       
    
    def get(self, *args, **kwargs):          
        if self.model.objects.filter(student=self.request.user).exists():
            return redirect('accountdetails')
        else:
            return super(PaymentStatus, self).get(*args, **kwargs) 
        
    def form_valid(self, form):
        form.instance.student = self.request.user
        self.request.user = form.save(commit =True)
        return super(PaymentStatus, self).form_valid(form)
    
    
    
    def get_success_url(self):
        pk = Payment_info.objects.get(student= self.request.user)
        return reverse_lazy('accountdetails')   
 

class AcctDetails(LoginRequiredMixin, ListView):
    model = Payment_info
    template_name ='accountdetails.html'
    fields =['session', 'percentage'] 
    context_object_name ='paymentstatus'
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['paid2'] = Payment_info.objects.filter(paid = 1).filter(student = self.request.user)
            return context        
    
    
class UpdateCourseReg(LoginRequiredMixin, UpdateView):
    model = Exam
    fields = [ 'course']
    template_name = 'coursereg_form.html'

    def get_success_url(self):
        
        return reverse_lazy('coursereg')
    
    def form_valid(self, form):
        form.instance.student_username= self.request.user
        self.request.user = form.save(commit =True)
        return super(UpdateCourseReg, self).form_valid(form)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        
        return context       
        


'''class Compilation(DetailView):
    model = Allcourses
    template_name = 'compute.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['trial'] =   self.object.registercoursename.all()
        
        return context  '''  
    
    
def Compilation(request, pk):
    lete =Allcourses.objects.get(pk=pk)
    lety =Allcourses.objects.get(pk=pk)
    trial =   lety.registercoursename.all()
    
    
    context = {
        'trial': trial,
        'lete': lete,
        }
    return render(request, 'compute.html', context)
   
   
class GenResult(LoginRequiredMixin, CreateView):
    model = Exam
    fields = [ 'student_username', 'course', 'scores']
    template_name = 'genresult.html'
    context_object_name ='general'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['JSS1'] = Exam.objects.all().order_by('student_username')
        context['courseregs'] = Exam.objects.all()
        
        return context           
    
    def get_success_url(self):
        return reverse_lazy('genresult')
    
class AboutUs(LoginRequiredMixin,  ListView):
    model = CustomUser
    template_name = 'aboutus.html' 
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['courseregs'] = Exam.objects.filter(student_username =self.request.user)

            return context     
             
        
class AssignedTeachers(LoginRequiredMixin,  ListView):
    model = Allcourses
    template_name = 'teacherlist.html' 
    
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            context['teacherlist'] = Allcourses.objects.all
            
            return context          


    
class UpdateAssignTeachers(LoginRequiredMixin,  UpdateView):
    form_class =TeachersForm
    model = Allcourses
    template_name = 'teachers_form.html' 
    
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logo'] = Logo.objects.all()
            
            return context          

    def form_valid(self, form):
        self.request.user = form.save(commit =True)
        return super(UpdateAssignTeachers, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('assignteachers')
    
def ViewPDF(request, pk):
    response =HttpResponse(content_type ='text/csv')
    response['Content-Disposition']='attachment; filename=result.csv'
    writer =csv.writer(response)
    lete =Allcourses.objects.get(pk=pk)
    data = lete.registercoursename.all()
    writer.writerow(['Name','Course','C.A score', 'Exam Score', 'Total Score'])
    for row in data:
        writer.writerow([row.student_username, row.course, row.cum_score, row.scores, row.total_score])
    return response


class GeneratePDF(DetailView):
    
    def get(self, request, pk):
        lete =Allcourses.objects.get(pk=pk)
        result =  lete.registercoursename.all()
        params = {
            'result': result,
            'request': request,
            'lete': lete
        }
        return Render.render('generatepdf.html', params)