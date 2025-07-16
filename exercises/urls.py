# urls.py placeholder
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_exercises', views.add_exercise, name='add_exercise'),
    path('', views.list_exercises, name='list_exercises'),
    path('edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
]
