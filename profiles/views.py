
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, FormView, ListView, DetailView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from . import models
from .models import Exam, Level, PostComments, Posts, Staffdata, Allcourses, Departments, CustomUser, Student_field, Logo
from django.contrib.auth import login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm



class UserList(LoginRequiredMixin,  ListView):
    model = CustomUser
    template_name ='users.html'
    context_object_name = 'userlist'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        
        return context
    
class Userdetail(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name ='userdetails.html'
    context_object_name = 'userdetail'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        #context['usercomplains'] = self.object.teachername.filter(resolved=True)
        context['usercomplains'] = self.object.teachername.all
     
        return context
        
    
    
class Postlist(ListView):
    model = Posts
    template_name ='pubs.html'
    context_object_name = 'posts'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['publications']= Posts.objects.all()
        return context


def post_detail(request, slug):
    #similar posts starts here
    pub = Posts.objects.get(slug=slug)
    #comment starts here
    post = get_object_or_404(Posts, slug=slug)
    comments = pub.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.author =request.user
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'pub': pub,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'details.html', context)
    

'''class Postdetail(DetailView):
    model = Posts
    template_name ='details.html'
    context_object_name = 'pub'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['publications']= Posts.objects.all()
        context['comments']= self.object.comments.filter(active=True)
        
        return context'''
    
    
class PubCreate(LoginRequiredMixin,  CreateView):
    model = Posts
    template_name ='createpub.html'
    fields = ['title', 'description', 'image']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('portal')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PubCreate, self).form_valid(form)
 
class UpdatePub(LoginRequiredMixin,  UpdateView):
    model = Posts
    fields = ['title', 'description', 'image']
    template_name ='createpub.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('portal')
       
    
class DeletePub(LoginRequiredMixin,  DeleteView):
    model = Posts
    template_name ='deletepub.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('portal')

      
class Home(ListView):
    model = Student_field
    template_name ='home.html'
    context_object_name = 'studentfields'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()


        return context
    
class Field(ListView):
    model = Student_field
    template_name ='fields.html'
    context_object_name = 'studentfields'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all()
        context['subjects'] = Allcourses.objects.all().order_by('field')
        context['subjects1'] = Allcourses.objects.filter(field= '1')
        context['subjects2'] = Allcourses.objects.filter(field= 2)
        context['subjects3'] = Allcourses.objects.filter(field= 3)
        context['subjects4'] = Allcourses.objects.filter(field= "4")
        context['publications'] = Posts.objects.all()

        return context    
    




class Register(CreateView):
    model = CustomUser
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'state', 'phone', 'country', 'mailing_address']
    template_name = 'register.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('portal')
    
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(
            form.cleaned_data["password"]
        )
        user=form.save(commit=True)
        if user is not  None:
            login(self.request, user)
        return super(Register, self).form_valid(form)
    
class UpdateUser(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'password', 'profile_pic', 'first_name', 'last_name',  'email', 'phone', 'state', 'country', 'is_student', 'is_teacher', 'is_superuser', 'class_enrolled', 'study_field', 'mailing_address']
    template_name = 'register.html'
    redirect_authenticated_user = True
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('portal')
        else:
            return super(UpdateUser, self).get(*args, **kwargs)

    
    def get_success_url(self):
        return reverse_lazy('userlist')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(
            form.cleaned_data["password"]
        )
        user=form.save(commit=True)
        '''
        #This is the code block that allows admin to login as any user from the backend
        
        if user is not  None:
            login(self.request, user)'''
        return super(UpdateUser, self).form_valid(form)


class DeleteUser(LoginRequiredMixin,  DeleteView):
    model = CustomUser
    template_name ='deleteuser.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('userlist')
      
    
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    
class CustomLogout(LogoutView):
   pass 
    
    
class Department(ListView):
    model = Departments
    template_name ='department.html'
    context_object_name = 'departments'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        context['publications'] = Posts.objects.all()

        return context    
    
          
class Deptstaff(DetailView):
    model = Departments
    template_name = 'deptstaffs.html'
    context_object_name = 'deptstaffs'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        context['publications'] = Posts.objects.all()
        context['deptstaffs'] = self.object.deptstaff.all()
        
        return context 
                 
class Staffs(ListView):
    model = Staffdata
    template_name ='staffs.html'
    context_object_name = 'staffs'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        context['publications'] = Posts.objects.all()
        context['teachers'] = CustomUser.objects.filter(is_teacher = True)

        return context    


class Teacherdetail(DetailView):
    model = CustomUser
    template_name ='teacherdetails.html'
    context_object_name = 'teacherdetails'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        context['publications'] = Posts.objects.all()
        context['teachers'] = CustomUser.objects.filter(is_teacher =True)
        context['details'] = self.object.course_teacher.all()

        return context    
   
class Level(ListView):
    model = Level
    template_name ='levels.html'
    context_object_name = 'levels'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = Logo.objects.all() 
        context['publications'] = Posts.objects.all()
        
        return context 
              