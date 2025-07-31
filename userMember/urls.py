from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_register, name='register'),    
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('accounts/', include('allauth.urls')),  
    path('trial', views.trial_stuffs, name = 'trial_stuffs'), 
    path('forget_password', views.forget_password, name ='forget_password'),
    path('password_reset', views.password_reset, name = 'password_reset'),


]
