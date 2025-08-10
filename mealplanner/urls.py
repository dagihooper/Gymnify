from django.urls import path, include
from . import views

urlpatterns = [
  path('nutrition_planner', views.nutrition_planner, name = 'nutrition_planner'),
  path('additional_info', views.addition_info, name = 'additional_info'),
  ]
