# urls.py placeholder
# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_exercises', views.add_exercise, name='add_exercise'),
    path('list_exercise', views.list_exercises, name='list_exercises'),
    path('edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('alternatives/', views.alternative_list, name='alternative_list'),
    path('alternatives/<int:pk>/', views.alternative_detail, name='alternative_detail')
]
