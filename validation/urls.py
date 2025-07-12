from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('insertion', views.insertion, name = 'insertion'),
    path('validation', views.validation, name = 'validation'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path("__reload__/", include("django_browser_reload.urls"))

]
