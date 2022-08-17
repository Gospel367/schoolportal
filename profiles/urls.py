from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.Register.as_view(), name= 'register'),
    path('', views.Home.as_view(), name= 'home'),
    path('fields/', views.Field.as_view(), name= 'fields'),
    path('departments/',views.Department.as_view(), name= 'departments'),
    path('departments/<slug>/', views.Deptstaff.as_view(), name= 'deptstaffs'),
    path('teacherdetails/<pk>/', views.Teacherdetail.as_view(), name= 'teacherdetails'),
    path('staffs/', views.Staffs.as_view(), name= 'staffs'),
    path('levels/', views.Level.as_view(), name= 'levels'),
    path('login/', views.CustomLoginView.as_view(next_page='portal'), name= 'login'),
    path('logout/', views.CustomLogout.as_view(next_page='home'), name= 'logout'),
    path('publications/', views.Postlist.as_view(), name= 'publist'),
    #path('publications/<slug>/', views.Postdetail.as_view(), name= 'details'),
    path('publications/<slug>/', views.post_detail, name= 'details'),
    path('createpub/', views.PubCreate.as_view(), name= 'createpub'),
    path('delete-pub/<int:pk>', views.DeletePub.as_view(), name ='deletepub'),
    path('update-pub/<int:pk>', views.UpdatePub.as_view(), name ='updatepub'),
    path('users/', views.UserList.as_view(), name= 'userlist'),
    path('users/<int:pk>/', views.Userdetail.as_view(), name= 'userdetail'),
    path('update-user/<int:pk>', views.UpdateUser.as_view(), name ='updateuser'),
    path('delete-user/<int:pk>', views.DeleteUser.as_view(), name ='deleteuser'),


    



]


